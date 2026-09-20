import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend, Rate } from 'k6/metrics';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

const responseSize = new Trend('response_size_bytes');
const paginationErrors = new Rate('pagination_errors');

export const options = {
    scenarios: {
        without_pagination: {
            executor: 'ramping-vus',
            startVUs: 0,
            stages: [
                { duration: '10s', target: 10 },
                { duration: '20s', target: 10 },
                { duration: '0s', target: 0 },
            ],
            exec: 'withoutPagination',
        },

        with_pagination: {
            executor: 'ramping-vus',
            startVUs: 0,
            stages: [
                { duration: '10s', target: 10 },
                { duration: '20s', target: 10 },
                { duration: '0s', target: 0 },
            ],
            exec: 'withPagination',
        },
    },

    thresholds: {
        http_req_failed: ['rate<0.01'],
        http_req_duration: ['p(95)<1000'],
        response_size_bytes: ['p(95)>0'],
        pagination_errors: ['rate<0.01'],
    },
};

function requestAndMeasure(url, scenario) {
    const response = http.get(url, {
        tags: {
            benchmark: 'BENCH-003',
            scenario: scenario,
        },
    });

    const bodySize = response.body ? response.body.length : 0;

    responseSize.add(bodySize, {
        scenario: scenario,
    });

    const successfulResponse = check(response, {
        'status is 200': (r) => r.status === 200,
        'response body is not empty': (r) => r.body.length > 0,
    });

    paginationErrors.add(!successfulResponse, {
        scenario: scenario,
    });

    sleep(1);
}

export function withoutPagination() {
    requestAndMeasure(
        `${BASE_URL}/api/products/`,
        'without_pagination'
    );
}

export function withPagination() {
    requestAndMeasure(
        `${BASE_URL}/api/products/?page=1&page_size=20`,
        'with_pagination'
    );
}
