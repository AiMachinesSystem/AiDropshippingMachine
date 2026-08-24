import { assertEquals, assertRejects } from "@std/assert";
import {
  createEbaySignatureVerifier,
  type EbaySdkSignatureValidator,
} from "./signature.ts";

Deno.test("uses the ECC validator without logging buyer PII", async () => {
  const calls: unknown[] = [];
  const logLines: unknown[][] = [];
  const originalLog = console.log;
  console.log = (...args: unknown[]) => logLines.push(args);

  try {
    const validate: EbaySdkSignatureValidator = (
      payload,
      signature,
      config,
    ) => {
      calls.push({ payload, signature, config });
      return Promise.resolve(true);
    };
    const verify = createEbaySignatureVerifier(
      "production-client-id",
      "production-client-secret",
      validate,
    );

    assertEquals(
      await verify({ notification: { data: { userId: "buyer-pii" } } }, "sig"),
      true,
    );
    assertEquals(calls, [{
      payload: { notification: { data: { userId: "buyer-pii" } } },
      signature: "sig",
      config: {
        clientId: "production-client-id",
        clientSecret: "production-client-secret",
        environment: "PRODUCTION",
      },
    }]);
    assertEquals(logLines, []);
  } finally {
    console.log = originalLog;
  }
});

Deno.test("suppresses SDK OAuth errors and restores the logger", async () => {
  const errorLines: unknown[][] = [];
  const originalError = console.error;
  const testLogger = (...args: unknown[]) => errorLines.push(args);
  console.error = testLogger;

  try {
    const validate: EbaySdkSignatureValidator = () => {
      console.error("sensitive SDK error");
      return Promise.reject(new Error("validator unavailable"));
    };
    const verify = createEbaySignatureVerifier("client", "secret", validate);

    await assertRejects(
      () => verify({}, "sig"),
      Error,
      "validator unavailable",
    );
    assertEquals(errorLines, []);
    assertEquals(console.error, testLogger);
  } finally {
    console.error = originalError;
  }
});
