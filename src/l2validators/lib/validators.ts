import axios from "axios";
const claimableAccountID = `GATFL2VALIDATORAPPLICATIONAAAAAAAAAAAAAAAAAAAAAAAAAAA4TT`
export async function getValidatorApplications() {
    const res = await axios.get(`https://horizon.stellar.org/claimable_balances?claimant=${claimableAccountID}`)
        .then(res => res.data._embedded.records)
    return res
}