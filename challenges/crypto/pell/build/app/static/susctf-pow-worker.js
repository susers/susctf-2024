import init, { calculate_proof } from './pkg/susctf_pow.js';

self.report_progress = function (progress) {
    self.postMessage({
        type: "progress",
        value: progress
    });
};

self.report_rate = function (rate) {
    self.postMessage({
        type: "rate",
        value: rate
    });
};

onmessage = function ({ data }) {
    const { answer, token } = data

    init().then(() => {
        const proof = calculate_proof(JSON.stringify(answer), token, 21)
        postMessage({
            type: "result",
            value: proof
        })
    })
}
