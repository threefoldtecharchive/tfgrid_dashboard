import dashboardPage from "../page-objects/dashboard-page"
import DashboardPage from "../page-objects/dashboard-page"





describe('TF Grid Dashboard', function(){


    this.beforeEach(function(){
        dashboardPage.Visit()
    })

    it("check the drop down menu",function(){
        /**************************************************
        Test Suite: TF Grid Dashboard
        Test Cases: TC823 - Verify drop down menu of explorer
        Scenario:
            - Verify the items appearing in the drop down menu
             from explorer in the dashboard
        **************************************************/
        dashboardPage.getSideMenu.click()
        dashboardPage.getExplorerBtn.click()
        cy.get('[href="/explorer/statistics"] > .v-list-item__content > .v-list-item__title').should('contain.text','Statistics')
        cy.xpath('//*[@id="app"]/div[1]/nav/div[1]/div/div[3]/div[2]/div/a[2]/div[2]/div').should('contain.text','Nodes')
        cy.xpath('//*[@id="app"]/div[1]/nav/div[1]/div/div[3]/div[2]/div/a[3]/div[2]/div').should('contain.text','Farms')

    })
    it("verify stats page",function(){
        /**************************************************
        Test Suite: TF Grid Dashboard
        Test Cases: TC823 - Verify Statistics
        Scenario:
            - Verify the values appearing in the statistics
            page from the grid proxy
        **************************************************/
        cy.get('.v-avatar > .v-image > .v-responsive__content').click()
        cy.get(':nth-child(4) > .v-list-group__header').click()
        cy.get('[href="/explorer/statistics"] > .v-list-item__content > .v-list-item__title').should('contain.text','Statistics').click()
        cy.get(':nth-child(1) > .item > .item__img > .item__title').should('contain.text','Nodes Online')

    })
    it("verify Nodes page",function(){
        /**************************************************
        Test Suite: TF Grid Dashboard
        Test Cases: TC823 - Verify Statistics
        Scenario:
            - Verify the values appearing in the statistics
            page from the grid proxy
        **************************************************/
        cy.get('.v-avatar > .v-image > .v-responsive__content').click()
        cy.get(':nth-child(4) > .v-list-group__header').click()
        cy.xpath('//*[@id="app"]/div[1]/nav/div[1]/div/div[3]/div[2]/div/a[2]/div[2]/div').should('contain.text','Nodes').click()
        cy.get('.v-alert__content').should('contain.text','Node statuses are updated every 2 hours.')

    })
    it("verify stats page",function(){
        /**************************************************
        Test Suite: TF Grid Dashboard
        Test Cases: TC823 - Verify Statistics
        Scenario:
            - Verify the values appearing in the statistics
            page from the grid proxy
        **************************************************/
        cy.get('.v-avatar > .v-image > .v-responsive__content').click()
        cy.get(':nth-child(4) > .v-list-group__header').click()
        cy.xpath('//*[@id="app"]/div[1]/nav/div[1]/div/div[3]/div[2]/div/a[3]/div[2]/div').should('contain.text','Farms').click()
        cy.get(':nth-child(1) > .v-card > .v-subheader').should('contain.text','FILTER BY FARM ID')

    })
})
