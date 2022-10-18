/// <reference types="cypress"/>

import FarmsPage from "../page-objects/farms-page"
import utils from "../utils/utils"


describe('TF Grid Dashboard', function(){


    this.beforeEach(function(){
        FarmsPage.Visit()
    })

    it("verify all nodes",function(){
        FarmsPage.Visit()
        
        cy.wait(2000)
        let x=1
        let y=1
    
        cy.get('tbody > :nth-child(1) > :nth-child(1)',{timeout:4500})
        cy
            .get('.text-start')
            .then( items =>
                {
            
                for (let i = 1; i < items.length; i++) 
                {
                    cy.request({
                        method: 'GET',
                        url:'https://gridproxy.dev.grid.tf/farms?farm_id='+items[i].innerText,

                    }).should((res)=>{
                        let farmid= JSON.stringify(res.body.farmId)
                        let farmname   = JSON.stringify(res.body.name)
                        let certyp   = JSON.stringify(res.body.certificationType)


                        cy
                        .get('tbody > :nth-child(1) > :nth-child('+i+')')
                        .should('contain.text',farmid)

                    })
                }
            })
        })
})
