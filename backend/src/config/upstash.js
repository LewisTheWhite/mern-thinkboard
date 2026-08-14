import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

import dotenv from 'dotenv';

dotenv.config();

// Create a new ratelimiter, that allows 50 requests per 20 seconds
const ratelimit = new Ratelimit({
    redis: Redis.fromEnv(),
    limiter: Ratelimit.slidingWindow(50, '20 s'),
});

export default ratelimit;

