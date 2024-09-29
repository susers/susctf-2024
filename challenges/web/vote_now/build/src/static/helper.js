export function calculateProof(answer, token, callback) {
    return new Promise((resolve, reject) => {
        const worker = new Worker("/static/susctf-pow-worker.js", { type: "module" })

        worker.onmessage = function (event) {
            const { type, value } = event.data
            if (type === "msg") {
                callback && callback(value)
            } else if (type === "result") {
                callback && callback(-1)
                resolve(value)
                worker.terminate()
            }
        }

        worker.onerror = function (event) {
            callback && callback(-1)
            reject(event)
            worker.terminate()
        }

        worker.postMessage({ answer, token, difficulty: 20 })
    })
}
