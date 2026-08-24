import type { SignatureVerifier } from "./app.ts";

export type EbaySdkSignatureValidator = (
  payload: unknown,
  signature: string,
  config: {
    clientId: string;
    clientSecret: string;
    environment: "PRODUCTION";
  },
) => Promise<boolean>;

/**
 * Adapt only the SDK's ECC validator.
 *
 * Do not call the SDK's public `process()` helper: its bundled account deletion
 * processor writes the buyer userId and username to console logs.
 */
export function createEbaySignatureVerifier(
  clientId: string,
  clientSecret: string,
  validateSignature: EbaySdkSignatureValidator,
): SignatureVerifier {
  const config = Object.freeze({
    clientId,
    clientSecret,
    environment: "PRODUCTION" as const,
  });
  let validationTail: Promise<void> = Promise.resolve();

  return async (payload: unknown, signature: string): Promise<boolean> => {
    let release: () => void = () => {};
    const previous = validationTail;
    validationTail = new Promise<void>((resolve) => {
      release = resolve;
    });
    await previous;

    // The SDK's OAuth client logs its complete error object before throwing.
    // Serialize validation and suppress that logger so credentials and request
    // metadata cannot enter Deno logs. The handler returns a generic 503.
    const originalError = console.error;
    console.error = () => {};
    try {
      return await validateSignature(payload, signature, config);
    } finally {
      console.error = originalError;
      release();
    }
  };
}
