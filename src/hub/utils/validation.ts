function checkKeplr(): Promise<any> {
    return new Promise((res, rej) => {
        function _checkKeplr() {
            if (window.keplr) res(window.keplr);
            else if (document.readyState == "complete") {
                rej("Keplr is not installed");
            } else {
                setTimeout(_checkKeplr, 500);
            }
        }
        _checkKeplr();
    });
}


async function ensureKeplr(chain_id: string): Promise<any> {
    let offlineSigner: any;
    return checkKeplr()
        .then((_) => {
            return window.keplr.getOfflineSigner(chain_id)
        })
        .then((signer) => {
            offlineSigner = signer
            return signer.getAccounts()
        })
        .then(() => {
            return offlineSigner
        })
        .catch((reason) => {
            if (reason.toString().indexOf("key not found") != -1) {
                throw new Error("Make sure there's at least one account configured in keplr")
            } else {
                throw reason
            }
        })
}

export {
    ensureKeplr,
    checkKeplr
}