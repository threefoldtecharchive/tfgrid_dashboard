/// <reference types="cypress"/>

import statsPage from "../page-objects/stats-page"
import utils from "../utils/utils"


describe('TF Grid Dashboard', function(){


    this.beforeEach(function(){
        statsPage.Visit()
    })


    it('Verify Statistics', function(){

        /**************************************************
        Test Suite: TF Grid Dashboard
        Test Cases: TC823 - Verify Statistics
        Scenario:
            - Verify the values appearing in the statistics
            page from the grid proxy
        **************************************************/

        cy.request({
            method: 'GET',
            url:'https://gridproxy.qa.grid.tf/stats?status=up',

        }).should((res)=>{
            
            //Get the stats from the grid_proxy
            let nodesOnline = JSON.stringify(res.body.nodes)
            let farms       = JSON.stringify(res.body.farms)
            let countries   = JSON.stringify(res.body.countries)
            let totalCru    = JSON.stringify(res.body.totalCru)
            let totalHru    = utils.formatBytes(JSON.stringify(res.body.totalHru))
            let totalSru    = utils.formatBytes(JSON.stringify(res.body.totalSru))
            let totalMru    = utils.formatBytes(JSON.stringify(res.body.totalMru))
            let accessNodes = JSON.stringify(res.body.accessNodes)
            let gateways    = JSON.stringify(res.body.gateways)
            let twins       = JSON.stringify(res.body.twins)
            let publicIps   = JSON.stringify(res.body.publicIps)
            let contracts   = JSON.stringify(res.body.contracts)

            //Verify the values appearing in the statisticspage from the grid proxy
            statsPage.VerifyStats(nodesOnline, farms, countries, totalCru, totalSru,
                totalHru, totalMru, accessNodes, gateways, twins, publicIps, contracts)
        })
        
    })

})