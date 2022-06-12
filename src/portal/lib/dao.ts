
import { hex2a } from './util'
import moment from 'moment'

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
    console.log(proposals)
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