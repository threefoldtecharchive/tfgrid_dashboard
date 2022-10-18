
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



Visit(){
   return cy.visit("/")
}


}
export default new DashboardPage();

