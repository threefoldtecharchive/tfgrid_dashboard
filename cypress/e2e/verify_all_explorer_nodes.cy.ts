/// <reference types="cypress"/>

import NodesPage from "../page-objects/nodes-page"
import utils from "../utils/utils"


describe('TF Grid Dashboard', function(){


    this.beforeEach(function(){
        NodesPage.Visit()
    })

    it("verify all nodes",function(){
        NodesPage.Visit()
        
        cy.wait(2000)
        NodesPage.getAllNodes
        let x=1
        let y=1
    
        cy.get('tbody > :nth-child(1) > .text-start',{timeout:4500})
        cy
            .get('.text-start')
            .then( items =>
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
                        if(i==1)
                        {
                            cy
                                .get('tbody > :nth-child(1) > .text-start')
                                .should('have.text',nodeId)
                            cy
                                .get('tbody > :nth-child(1) > :nth-child(2)')
                                .should('have.text',farmid)
                        }
                        else
                        {
                            cy
                                .get(':nth-child('+i+') > .text-start')
                                .should('have.text',nodeId)
                            cy
                                .get('tbody > :nth-child('+i+') > :nth-child(2)')
                                .should('have.text',farmid)
                        }
                        cy
                        .xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/tbody/tr['+i+']/td[5]')
                        .then(hruItem =>
                            {
                                console.log(hruItem)
                                if(Number(hruItem[0].innerText)==0)
                                {
                                }
                                else
                                {
                                cy
                                .xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/tbody/tr['+i+']/td[5]')
                                .should('contain.text',HRU)
                                }
                            })

                            cy
                            .xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/tbody/tr['+i+']/td[6]')
                            .should('contain.text',SRU)
                            cy
                            .xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/tbody/tr['+i+']/td[7]')
                            .should('contain.text',MRU)
                            cy
                            .xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/tbody/tr['+i+']/td[8]')
                            .should('contain.text',CRU)
                    })
                }
            })
        })
})
