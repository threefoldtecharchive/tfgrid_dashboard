/// <reference types="cypress"/>

import FarmsPage from "../page-objects/farms-page"
import utils from "../utils/utils"


describe('TF Grid Dashboard', function(){


    this.beforeEach(function(){
        FarmsPage.Visit()
    })

    it("verify all nodes",function(){
        
        cy.wait(4500)
        let x=1
        let y=1
    
        cy.get('tbody > :nth-child(1) > :nth-child(1)',{timeout:4500})
        
                for (let i = 1; i < 15; i++) 
                {

                    cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div/div[1]/table/tbody/tr['+i+']/td[1]')
                    .then (item =>
                    cy.request({
                        method: 'GET',
                        url:'https://gridproxy.dev.grid.tf/farms?farm_id='+item[0].innerText,

                    }).should((res)=>{
                        let farmid= JSON.stringify(res.body[i].farmId)
                        let farmname   = (res.body[i].name)
                        let certyp   = (res.body[i].certificationType)


                        cy
                        .get('tbody > :nth-child('+i+') > :nth-child(1)')
                        .contains(farmid)

                        cy
                        .get('tbody > :nth-child('+i+') > :nth-child(2)')
                        .contains(farmname)

                        cy
                        .get('tbody > :nth-child('+i+') > :nth-child(6)')
                        .contains(certyp)
                })
                    )


                    }})
                })