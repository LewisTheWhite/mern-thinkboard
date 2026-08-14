import ratelimit from "../config/upstash.js";

const getClientIp = (req) => {
    const forwarded = req.headers["x-forwarded-for"];
    if (typeof forwarded === "string" && forwarded.length > 0) {
        return forwarded.split(",")[0].trim();
    }

    if (Array.isArray(forwarded) && forwarded.length > 0) {
        return forwarded[0];
    }

    return req.ip || req.socket?.remoteAddress || "unknown";
};

const parseBooleanEnv = (value) => {
    if (typeof value !== "string") {
        return undefined;
    }

    if (value.toLowerCase() === "true") {
        return true;
    }

    if (value.toLowerCase() === "false") {
        return false;
    }

    return undefined;
};

const rateLimiter = async (req, res, next) => {
    try {
        const clientIp = getClientIp(req);
        const { success } = await ratelimit.limit(`rate-limit:${clientIp}`); // Use request IP as key so limits are not shared globally
        
        if (!success) {
            return res.status(429).json({ message: "Too many requests. Please try again later." }); // If the user has exceeded the rate limit, return a 429 error
        }

        next();
    } catch (error) {
        const envFailOpen = parseBooleanEnv(process.env.RATE_LIMIT_FAIL_OPEN);
        const failOpen = envFailOpen ?? process.env.NODE_ENV !== "production";
        const upstashUrl = process.env.UPSTASH_REDIS_REST_URL || "";
        const upstashHost = upstashUrl ? new URL(upstashUrl).hostname : "missing";

        console.error("[RateLimiter] Upstash request failed", {
            method: req.method,
            path: req.originalUrl,
            clientIp: getClientIp(req),
            userAgent: req.headers["user-agent"] || "unknown",
            nodeEnv: process.env.NODE_ENV || "undefined",
            failOpen,
            upstashHost,
            hasUpstashToken: Boolean(process.env.UPSTASH_REDIS_REST_TOKEN),
            errorName: error?.name,
            errorMessage: error?.message,
            causeCode: error?.cause?.code,
            causeHostname: error?.cause?.hostname,
            causeMessage: error?.cause?.message,
        });

        if (failOpen) {
            console.warn("[RateLimiter] Bypassing rate limit for this request due to provider failure");
            return next();
        }

        return res.status(500).json({ message: "Internal server error" });
    }
}

export default rateLimiter;