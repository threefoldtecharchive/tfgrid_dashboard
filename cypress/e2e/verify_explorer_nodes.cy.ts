/// <reference types="cypress"/>

import { should } from "chai"
import nodesPage from "../page-objects/nodes-page"
import NodesPage from "../page-objects/nodes-page"
import utils from "../utils/utils"


describe('TF Grid Dashboard', function(){


    this.beforeEach(function(){
        NodesPage.Visit()
        cy.get('.v-data-footer__select > .v-input > .v-input__control > .v-input__slot > .v-select__slot > .v-input__append-inner > .v-input__icon > .v-icon').type("a{enter}")
    })

    it("verify all nodes",function(){

        cy
        .get('.text-start')
        .then( IDD =>{
            console.log(IDD)
        })
        cy
        .get('.text-center',)
        .then( item =>{
            console.log(item)
        })


        
        cy.request({
            method: 'GET',
            url:'https://gridproxy.dev.grid.tf/nodes/'+11,

        }).should((res)=>{
            let nodeId = JSON.stringify(res.body.nodeId)
            let farmid= JSON.stringify(res.body.farmId)
            let HRU   = utils.formatBytes(JSON.stringify(res.body.capacity.total_resources.hru))
            let SRU   = utils.formatBytes(res.body.capacity.total_resources.sru)
            let MRU   = utils.formatBytes(res.body.capacity.total_resources.mru)
            let CRU   = utils.formatBytes(res.body.capacity.total_resources.cru)
           
            //Verify the values appearing in the Nodespage from the grid proxy
            NodesPage.VerifyNodes(nodeId, farmid, HRU, SRU, MRU, CRU)
    })
    it("check sorting",function(){
        NodesPage.Visit()
        cy.get('.v-data-footer__select > .v-input > .v-input__control > .v-input__slot > .v-select__slot > .v-input__append-inner > .v-input__icon > .v-icon').type("a{enter}")


    })
})
})
