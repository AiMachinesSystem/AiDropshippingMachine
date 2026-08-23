export interface ApiRequest {
  method: "GET" | "POST" | "PUT";
  path: string;
  body?: unknown;
  write: boolean;
  idempotencyKey?: string;
}

export interface TokenProvider {
  get(): Promise<string>;
  refresh(): Promise<string>;
}

export interface EbayApiClientOptions {
  baseUrl: string;
  marketplaceId: string;
  locale: string;
  tokenProvider: TokenProvider;
  fetcher?: typeof fetch;
  max5xxRetries?: number;
  max429Retries?: number;
  baseDelayMs?: number;
  delay?: (ms: number) => Promise<void>;
}

export class EbayApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly errorIds: number[] = [],
    readonly domains: string[] = [],
    readonly categories: string[] = [],
  ) {
    super(message);
    this.name = "EbayApiError";
  }
}

const PUBLISH_PATH = /\/publish/;

export class EbayApiClient {
  readonly baseUrl: string;
  private readonly marketplaceId: string;
  private readonly locale: string;
  private readonly tokenProvider: TokenProvider;
  private readonly fetcher: typeof fetch;
  private readonly max5xxRetries: number;
  private readonly max429Retries: number;
  private readonly baseDelayMs: number;
  private readonly delayFn: (ms: number) => Promise<void>;

  constructor(options: EbayApiClientOptions) {
    this.baseUrl = options.baseUrl;
    this.marketplaceId = options.marketplaceId;
    this.locale = options.locale;
    this.tokenProvider = options.tokenProvider;
    this.fetcher = options.fetcher ?? fetch;
    this.max5xxRetries = options.max5xxRetries ?? 3;
    this.max429Retries = options.max429Retries ?? 3;
    this.baseDelayMs = options.baseDelayMs ?? 200;
    this.delayFn = options.delay ??
      ((ms) => new Promise((resolve) => setTimeout(resolve, ms)));
  }

  async request<T>(req: ApiRequest): Promise<T> {
    let usedRefresh = false;
    let fiveXx = 0;
    let four29 = 0;
    const isPublish = PUBLISH_PATH.test(req.path);

    while (true) {
      const response = await this.rawFetch(req);
      const status = response.status;

      if (status === 401 && !usedRefresh) {
        usedRefresh = true;
        await this.tokenProvider.refresh();
        continue;
      }

      if (status === 401 || status === 409) {
        throw await this.toError(response);
      }

      if (status === 429 && !isPublish && four29 < this.max429Retries) {
        four29++;
        const retryAfter = this.retryAfterSeconds(response);
        await this.delayFn(
          retryAfter > 0 ? retryAfter * 1000 : this.baseDelayMs * 2 ** four29,
        );
        continue;
      }

      if (status >= 500 && !isPublish && fiveXx < this.max5xxRetries) {
        fiveXx++;
        await this.delayFn(this.baseDelayMs * 2 ** (fiveXx - 1));
        continue;
      }

      if (!response.ok) {
        throw await this.toError(response);
      }

      return this.parseBody<T>(response);
    }
  }

  private async rawFetch(req: ApiRequest): Promise<Response> {
    const token = await this.tokenProvider.get();
    const headers: Record<string, string> = {
      "Authorization": `Bearer ${token}`,
      "Content-Language": this.locale,
      "Accept-Language": this.locale,
      "X-EBAY-C-MARKETPLACE-ID": this.marketplaceId,
    };
    if (req.body !== undefined) {
      headers["Content-Type"] = "application/json";
    }
    if (req.idempotencyKey) {
      headers["Idempotency-Key"] = req.idempotencyKey;
    }
    const init: RequestInit = { method: req.method, headers };
    if (req.body !== undefined) {
      init.body = JSON.stringify(req.body);
    }
    return this.fetcher(`${this.baseUrl}${req.path}`, init);
  }

  private retryAfterSeconds(response: Response): number {
    const header = response.headers.get("retry-after");
    if (!header) return 0;
    const seconds = Number(header);
    return Number.isFinite(seconds) && seconds >= 0 ? seconds : 0;
  }

  private async parseBody<T>(response: Response): Promise<T> {
    const text = await response.text();
    if (!text) return undefined as unknown as T;
    try {
      return JSON.parse(text) as T;
    } catch {
      return undefined as unknown as T;
    }
  }

  private async toError(response: Response): Promise<EbayApiError> {
    const status = response.status;
    let message = `eBay API error (HTTP ${status})`;
    let errorIds: number[] = [];
    let domains: string[] = [];
    let categories: string[] = [];
    const text = await response.text();
    try {
      const parsed = JSON.parse(text) as {
        errors?: Array<Record<string, unknown>>;
      };
      const errors = parsed.errors ?? [];
      errorIds = errors.map((e) => e.errorId).filter((
        v,
      ): v is number => typeof v === "number");
      domains = errors.map((e) => e.domain).filter((
        v,
      ): v is string => typeof v === "string");
      categories = errors.map((e) => e.category).filter((
        v,
      ): v is string => typeof v === "string");
      const first = errors[0];
      if (first) {
        message = String(first.longMessage ?? first.message ?? message);
      }
    } catch {
      // Keep the generic message when the body is not JSON.
    }
    return new EbayApiError(message, status, errorIds, domains, categories);
  }
}
