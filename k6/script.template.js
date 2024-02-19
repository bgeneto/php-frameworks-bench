import http from 'k6/http';
import { check } from 'k6';
import { sleep } from 'k6';

export const options = {
    scenarios: {
        breaking: {
            executor: "ramping-vus",
            gracefulRampDown: "2s",
            gracefulStop: '3s',
            stages: [
                { duration: "10s", target: 100 },
                { duration: "10s", target: 200 },
                { duration: "10s", target: 400 },
            ],
        },
    },
};

export default function () {
    const res = http.get('{{ URI }}');
    check(res, {
        'is status 200': (r) => r.status === 200,
    });
    sleep(1);
}

