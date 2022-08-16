/// <reference types="cypress"/>
/// <reference types="cypress-xpath"/>

class StatsPage{

    get getNodesCard(){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[2]/section/div[1]/div/div/p')
    }

    get getFarmsCard(){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[2]/section/div[2]/div/div/p')
    }

    get getCountriesCard(){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[2]/section/div[3]/div/div/p')
    }

    get getCpuCard(){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[2]/section/div[4]/div/div/p')
    }

    get getSsdCard(){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[2]/section/div[5]/div/div/p')
    }

    get getHddCard(){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[2]/section/div[6]/div/div/p')
    }

    get getRamCard(){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[2]/section/div[7]/div/div/p')
    }

    get getAccessNodesCard(){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[2]/section/div[8]/div/div/p')
    }

    get getGatewaysCard(){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[2]/section/div[9]/div/div/p')
    }

    get getTwinsCard(){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[2]/section/div[10]/div/div/p')
    }

    get getPublicIpsCard(){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[2]/section/div[11]/div/div/p')
    }

    get getContractsCard(){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[2]/section/div[12]/div/div/p')
    }

    // Navigate to the Statistics Page in the dashboard
    Visit(){
        return cy.visit("/explorer/statistics")
    }


    //Verify the stats of each card in the statistics page
    VerifyStats(nodes, farms, countries, cpu, ssd, hdd, ram, accessNodes,
        gateways, twins, publicIps, contracts){

        this.getNodesCard.contains(nodes)

        this.getFarmsCard.contains(farms)

        this.getCountriesCard.contains(countries)

        this.getCpuCard.contains(cpu)

        this.getSsdCard.contains(ssd)

        this.getHddCard.contains(hdd)

        this.getRamCard.contains(ram)

        this.getAccessNodesCard.contains(accessNodes)

        this.getGatewaysCard.contains(gateways)

        this.getTwinsCard.contains(twins)

        this.getPublicIpsCard.contains(publicIps)

        this.getContractsCard.contains(contracts)
    }

}

export default new StatsPage();