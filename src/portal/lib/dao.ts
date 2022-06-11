
import { hex2a } from './util'
import moment from 'moment'
export async function getProposals(api: any) {
    const hashes = await getProposalHashes(api)
    const parsedHashes = hashes.map(async (h: { toJSON: () => any }) => {
        const daoProposal = await getDaoProposal(api, h)
        daoProposal.description = hex2a(daoProposal.description)
        daoProposal.link = hex2a(daoProposal.link)

        const daoProposalMethod = await getDaoProposalMethod(api, h)
        const votes = await getDaoProposalVotes(api, h)
        if (votes) {
            const nowBlock = await api.query.system.number()
            const timeUntilEnd = (votes.end - nowBlock.toJSON()) * 6
            votes.timeUntilEnd = moment().add('second', timeUntilEnd)
            console.log(timeUntilEnd)
        }
        console.log(votes)
        return {
            hash: h.toJSON(),
            ...daoProposal,
            method: daoProposalMethod,
            ...votes,
        }
    })
    return await Promise.all(parsedHashes)
}
export async function getProposalHashes(api: { query: { dao: { proposalList: () => any } } }) {
    return await api.query.dao.proposalList()
}
export async function getDaoProposal(api: { query: any }, hash: { toJSON: () => any }) {
    const proposal = await api.query.dao.proposals(hash)
    return proposal.toJSON()
}
export async function getDaoProposalMethod(api: { query: any }, hash: { toJSON: () => any }) {
    const proposal = await api.query.dao.proposalOf(hash)
    return proposal.toJSON()
}
export async function getDaoProposalVotes(api: { query: any }, hash: { toJSON: () => any }) {
    const voting = await api.query.dao.voting(hash)
    return voting.toJSON()
}