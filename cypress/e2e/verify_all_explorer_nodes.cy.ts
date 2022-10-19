/// <reference types="cypress"/>

import NodesPage from "../page-objects/nodes-page"
import utils from "../utils/utils"


describe('TF Grid Dashboard', function(){


    this.beforeEach(function(){
        NodesPage.Visit()
    })

    it("verify all nodes",function(){
        /**************************************************
        Test Suite: TF Grid Dashboard
        Test Cases: TC1197 - Verify all nodes
        Scenario:
        - Verify the values appearing in the node
        page from the grid proxy
        **************************************************/
        NodesPage.Visit()
        
        cy.wait(2000)
        NodesPage.getAllNodes
        let x=1
        let y=1
    
        //collect all nodes in array
        cy.get('tbody > :nth-child(1) > .text-start',{timeout:4500})
        NodesPage.getArrayOfNodes.then( items =>
                {
            
                for (let i = 1; i < (items.length); i++) 
                {
                    cy.request({
                        method: 'GET',
                        url:'https://gridproxy.dev.grid.tf/nodes/'+items[i].innerText,

                    }).should((res)=>{
                        let nodeId = JSON.stringify(res.body.nodeId)
                        let farmid= JSON.stringify(res.body.farmId)
                        let HRU   = utils.formatBytes(JSON.stringify(res.body.capacity.total_resources.hru))
                        let SRU   = utils.formatBytes(res.body.capacity.total_resources.sru)
                        let MRU   = utils.formatBytes(res.body.capacity.total_resources.mru)
                        let CRU   = utils.formatBytes(res.body.capacity.total_resources.cru)

                        //verify nodes data
                        NodesPage.VerifyNodes(i,nodeId, farmid, SRU, MRU, CRU)
                        // verify nodes HRU
                        NodesPage.getHRU(i).then(hruItem =>
                            {
                                console.log(hruItem)
                                if(Number(hruItem[0].innerText)==0)
                                {
                                }
                                else
                                {
                                NodesPage.getHRU(i).should('contain.text',HRU)
                                }
                            })
                    })
                }
            })
        })
})
