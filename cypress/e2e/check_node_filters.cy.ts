/// <reference types="cypress"/>

import { should } from "chai"
import nodesPage from "../page-objects/nodes-page"
import NodesPage from "../page-objects/nodes-page"
import utils from "../utils/utils"
import dashboardPage from "../page-objects/dashboard-page"

describe('TF Grid Dashboard', function(){


    this.beforeEach(function(){
        NodesPage.Visit()
        cy.get('.v-data-footer__select > .v-input > .v-input__control > .v-input__slot > .v-select__slot > .v-input__append-inner > .v-input__icon > .v-icon').type("a{enter}")
    })

    it("verify Nodes page HRU filter",function(){
        /**************************************************
        Test Suite: TF Grid Dashboard
        Test Cases: TC1208 - Verify Nodes page filter
        Scenario:
            - Verify the you can reach the nodes
            page from the grid proxy
        **************************************************/
            dashboardPage.getSideMenu.click()
            dashboardPage.getExplorerBtn.click()
            dashboardPage.NodesBtn.click()
            cy.get('#input-68').click().type("10{enter}")
            cy.get('td').should('contain.text','No data available')
        

    })
    it("verify Nodes page MRU filter",function(){
        /**************************************************
        Test Suite: TF Grid Dashboard
        Test Cases: TC1196 - Verify Nodes page filter
        Scenario:
            - Verify the you can reach the nodes
            page from the grid proxy
        **************************************************/
            dashboardPage.getSideMenu.click()
            dashboardPage.getExplorerBtn.click()
            dashboardPage.NodesBtn.click()
            cy.get('#input-74').click().type("10{enter}")
            cy.get('td').should('contain.text','No data available')
        

    })
})