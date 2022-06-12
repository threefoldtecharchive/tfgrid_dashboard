
import { hex2a } from './util'
import moment from 'moment'
import { web3FromAddress } from '@polkadot/extension-dapp';
export async function vote(address: string, api: { tx: { dao: { vote: (arg0: any, arg1: any, arg2: any) => { (): any; new(): any; signAndSend: { (arg0: any, arg1: { signer: any }, arg2: any): any; new(): any } } } } }, farmId: string, hash: any, approve: any, callback: any) {
    try {
        const injector = await web3FromAddress(address)
        return api.tx.dao
            .vote(farmId, hash, approve)
            .signAndSend(address, { signer: injector.signer }, callback)
    } catch (error) {
        console.log(`err while trying to get injector ${error}`)
    }
}
export async function getProposals(api: any) {
    const proposals: any = [];
    const hashes = await api.query.dao.proposalList()
    hashes.map(async (hash: { toJSON: () => any; }) => {
        const daoProposal = await getDaoProposal(api, hash)
        const proposal = await getProposal(api, hash)
        const proposalVotes = await getProposalVotes(api, hash)

        proposals.push({
            threshold: proposalVotes.threshold,
            ayes: proposalVotes.ayes,
            nayes: proposalVotes.nayes,
            vetos: proposalVotes.vetos,
            end: proposalVotes.end,
            hash: hash,
            action: hex2a(proposal.args._remark),
            description: hex2a(daoProposal.description),
            link: hex2a(daoProposal.link)
        })
    })
    return proposals
}

export async function getDaoProposal(api: { query: any }, hash: { toJSON: () => any }) {
    const proposal = await api.query.dao.proposals(hash)
    return proposal.toJSON()
}
export async function getProposal(api: { query: any }, hash: { toJSON: () => any }) {
    const proposal = await api.query.dao.proposalOf(hash)
    return proposal.toJSON()
}
export async function getProposalVotes(api: any, hash: any) {
    const voting = await api.query.dao.voting(hash)
    return voting.toJSON()
}