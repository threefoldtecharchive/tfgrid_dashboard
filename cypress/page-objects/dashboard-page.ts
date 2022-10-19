
/// <reference types="cypress"/>
/// <reference types="cypress-xpath"/>

class DashboardPage{

    get getNodesId(){
        return cy.get('tbody > :nth-child(1) > .text-start')
    }
    get getSideMenu(){
        return cy.get('.v-avatar > .v-image > .v-responsive__content')
    }
    get getExplorerBtn(){
        return  cy.get(':nth-child(4) > .v-list-group__header')
    }
    get StatsBtn(){
        return         cy.get('[href="/explorer/statistics"] > .v-list-item__content > .v-list-item__title').should('contain.text','Statistics')

    }
    get NodesBtn(){
         return cy.xpath('//*[@id="app"]/div[1]/nav/div[1]/div/div[3]/div[2]/div/a[2]/div[2]/div').should('contain.text','Nodes')
    }

    get FarmsBtn(){
        return         cy.xpath('//*[@id="app"]/div[1]/nav/div[1]/div/div[3]/div[2]/div/a[3]/div[2]/div').should('contain.text','Farms')
   }


Visit(){
   return cy.visit("/")
}


}
export default new DashboardPage();

