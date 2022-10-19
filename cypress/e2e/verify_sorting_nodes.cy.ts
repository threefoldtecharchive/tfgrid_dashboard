/// <reference types="cypress"/>

import { should } from "chai"
import nodesPage from "../page-objects/nodes-page"
import NodesPage from "../page-objects/nodes-page"
import utils from "../utils/utils"


describe('TF Grid Dashboard', function(){


    this.beforeEach(function(){
        NodesPage.Visit()
        cy.wait(5500)
    })
    it("check sorting node-id asc",function(){
               /**************************************************
        Test Suite: TF Grid Dashboard
        Test Cases: TC1198 - sorting asc all nodes
        Scenario:
        - Verify the values appearing in the node
        page from the grid proxy
        **************************************************/
        
        nodesPage.getAllNodes
        nodesPage.ClickOnSortId
        let x=1
        let y=1
        cy.wait(200)
    
       nodesPage.getArrayOfNodes.then( items =>
                {
                for (let i = 1; i < (items.length-1); i++) {
                    y=Number(items[i+1].innerText)
                    x=Number(items[i].innerText)
                    expect(Number(y)).to.be.greaterThan(Number(x))
                }
                
            })
            
        })
        it("check sorting node-id desc",function(){
        /**************************************************
        Test Suite: TF Grid Dashboard
        Test Cases: TC1205 - sorting desc all nodes
        Scenario:
        - Verify the values appearing in the node
        page from the grid proxy
        **************************************************/
            
            nodesPage.getAllNodes
            nodesPage.ClickOnSortId
            nodesPage.ClickOnSortId

            let x=1
            let y=1
            console.log(x)
            console.log(y)
            cy.wait(200)
            nodesPage.getArrayOfNodes.then( items =>
                    {
                    
                    for (let i = 1; i < (items.length-1); i++) {

                        y=Number(items[i+1].innerText)
                        x=Number(items[i].innerText)

                        expect(Number(x)).to.be.greaterThan(Number(y))
                    }
                    
                })
                
            })
            it("check sorting farm-id desc",function(){
                NodesPage.Visit()
                
                nodesPage.getAllNodes
                nodesPage.ClickOnSortId
                nodesPage.ClickOnSortId
    
                let x=1
                let y=1
                console.log(x)
                console.log(y)
                cy.wait(200)
                nodesPage.getArrayOfNodes.then( items =>
                    {
                    
                    for (let i = 1; i < (items.length-1); i++) {

                        y=Number(nodesPage.getFarmId(i+1))
                        x=Number(nodesPage.getFarmId(i))


                        expect(Number(x)).to.be.greaterThan(Number(y))
                    }
                        
                    })
                    
                })
    });
    