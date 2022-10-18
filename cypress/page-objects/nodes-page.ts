/// <reference types="cypress"/>
/// <reference types="cypress-xpath"/>

class NodesPage{

    get getNodesId(){
        return cy.get('tbody > :nth-child(1) > .text-start')
    }

    get getFarmId(){
        return cy.get('tbody > :nth-child(2) > .text-start')
    }
    get getHRU(){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[5]')
    }
    get getSRU(){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[6]')
    }
    get getMRU(){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[7]')
    }
    get getCRU(){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[8]')
    }
    get getNodesIdk(){
        return cy.get('tbody > :nth-child(20) > .text-start')

    }
    get getAllNodes(){
        return cy.get('.v-data-footer__select > .v-input > .v-input__control > .v-input__slot > .v-select__slot > .v-input__append-inner > .v-input__icon > .v-icon').type("a{enter}")

    }

    // Navigate to the Nodes Page in the dashboard
    Visit(){
        return cy.visit('https://dashboard.dev.grid.tf/explorer/nodes')
    }

    //Verify the stats of each card in the nodes page
    VerifyNodes(NodeId, FarmId, HRU, SRU, MRU, CRU)
    {

        this.getNodesId.contains(NodeId)

        this.getFarmId.contains(FarmId)

        this.getHRU.contains(HRU)

        this.getSRU.contains(SRU)

        this.getMRU.contains(MRU)

        this.getCRU.contains(CRU)
    }

}

export default new NodesPage();

