/// <reference types="cypress"/>
/// <reference types="cypress-xpath"/>

class NodesPage{

    getNodesId(i){
        return                         cy
        .get(':nth-child('+i+') > .text-start')
    }

    getFarmId(i){
        return cy
        .get('tbody > :nth-child('+i+') > :nth-child(2)')
    }
    getHRU(i){
        return  cy
        .xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/tbody/tr['+i+']/td[5]')
    }
    getSRU(i){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/tbody/tr['+i+']/td[6]')
    }
    getMRU(i){
        return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/tbody/tr['+i+']/td[7]')
    }
    getCRU(i){
        return cy
        .xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/tbody/tr['+i+']/td[8]')
          }
    get getNodesIdk(){
        return cy.get('tbody > :nth-child(20) > .text-start')

    }
    get getAllNodes(){
        return cy.get('.v-data-footer__select > .v-input > .v-input__control > .v-input__slot > .v-select__slot > .v-input__append-inner > .v-input__icon > .v-icon').type("a{enter}")

    }
    get getArrayOfNodes(){
        return cy
        .get('.text-start')
    }
    get ClickOnSortId(){
         return cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/thead/tr/th[1]/i').click()

    }

    // Navigate to the Nodes Page in the dashboard
    Visit(){
        return cy.visit('https://dashboard.dev.grid.tf/explorer/nodes')
    }

    //Verify the stats of each card in the nodes page
    VerifyNodes(i,NodeId, FarmId, SRU, MRU, CRU)
    {

        this.getNodesId(i).contains(NodeId)

        this.getFarmId(i).contains(FarmId)

        // this.getHRU.contains(HRU)

        this.getSRU(i).contains(SRU)

        this.getMRU(i).contains(MRU)

        this.getCRU(i).contains(CRU)
    }

}

export default new NodesPage();

