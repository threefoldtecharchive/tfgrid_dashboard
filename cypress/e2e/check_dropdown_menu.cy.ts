import dashboardPage from "../page-objects/dashboard-page"
import DashboardPage from "../page-objects/dashboard-page"





describe('TF Grid Dashboard', function(){


    this.beforeEach(function(){
        dashboardPage.Visit()
    })

    it("check the drop down menu",function(){
        /**************************************************
        Test Suite: TF Grid Dashboard
        Test Cases: TC1193 - Verify drop down menu of explorer
        Scenario:
            - Verify the items appearing in the drop down menu
             from explorer in the dashboard
        **************************************************/
        dashboardPage.getSideMenu.click()
        dashboardPage.getExplorerBtn.click()
        dashboardPage.StatsBtn
        dashboardPage.NodesBtn
        cy.xpath('//*[@id="app"]/div[1]/nav/div[1]/div/div[3]/div[2]/div/a[3]/div[2]/div').should('contain.text','Farms')

    })
    it("verify stats page",function(){
        /**************************************************
        Test Suite: TF Grid Dashboard
        Test Cases: TC1194 - Verify Statistics page
        Scenario:
            - Verify the you can reach the statistics
            page from the grid proxy
        **************************************************/
        dashboardPage.getSideMenu.click()
        dashboardPage.getExplorerBtn.click()
        dashboardPage.StatsBtn.click()
        cy.get(':nth-child(1) > .item > .item__img > .item__title').should('contain.text','Nodes Online')

    })
    it("verify Nodes page",function(){
        /**************************************************
        Test Suite: TF Grid Dashboard
        Test Cases: TC1196 - Verify Nodes page
        Scenario:
            - Verify the you can reach the nodes
            page from the grid proxy
        **************************************************/
            dashboardPage.getSideMenu.click()
            dashboardPage.getExplorerBtn.click()
        dashboardPage.NodesBtn.click()
        cy.get('.v-alert__content').should('contain.text','Node statuses are updated every 2 hours.')

    })
    it("verify stats page",function(){
        /**************************************************
        Test Suite: TF Grid Dashboard
        Test Cases: TC1204 - Verify Farms page
        Scenario:
            - Verify the you can reach the Farms
            page from the grid proxy
        **************************************************/
            dashboardPage.getSideMenu.click()
            dashboardPage.getExplorerBtn.click()
        dashboardPage.FarmsBtn.click()
        cy.get(':nth-child(1) > .v-card > .v-subheader').should('contain.text','FILTER BY FARM ID')

    })
})
