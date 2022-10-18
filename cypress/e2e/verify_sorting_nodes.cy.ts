/// <reference types="cypress"/>

import { should } from "chai"
import nodesPage from "../page-objects/nodes-page"
import NodesPage from "../page-objects/nodes-page"
import utils from "../utils/utils"


describe('TF Grid Dashboard', function(){


    this.beforeEach(function(){
        NodesPage.Visit()
    })
    it("check sorting node-id asc",function(){
        NodesPage.Visit()
        
        cy.get('.v-data-footer__select > .v-input > .v-input__control > .v-input__slot > .v-select__slot > .v-input__append-inner > .v-input__icon > .v-icon').type("a{enter}")
        cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/thead/tr/th[1]/i').click()
        let x=1
        let y=1
        cy.wait(200)
    
        cy.get('tbody > :nth-child(1) > .text-start')

        cy
            .get('.text-start').should('be.visible')
            .eq(1)
            .should('have.text','11')

        cy
            .get('.text-start')
            .then( items =>
                {
                for (let i = 1; i < (items.length-1); i++) {
                    y=Number(items[i+1].innerText)
                    x=Number(items[i].innerText)
                    expect(Number(y)).to.be.greaterThan(Number(x))
                }
                
            })
            
        })
        it("check sorting node-id desc",function(){
            NodesPage.Visit()
            
            cy.get('.v-data-footer__select > .v-input > .v-input__control > .v-input__slot > .v-select__slot > .v-input__append-inner > .v-input__icon > .v-icon').type("a{enter}")
            cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/thead/tr/th[1]/i').click()
            cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/thead/tr/th[1]/i').click()

            let x=1
            let y=1
            console.log(x)
            console.log(y)
            cy.wait(200)
        
            cy.get('tbody > :nth-child(1) > .text-start')
    
            cy
                .get('.text-start').should('be.visible')
                .eq(1)
                .should('have.text','49')
    
            cy
                .get('.text-start')
                .then( items =>
                    {
                    
                    for (let i = 1; i < (items.length-1); i++) {

                        y=Number(items[i+1].innerText)
                        x=Number(items[i].innerText)

                        expect(Number(x)).to.be.greaterThan(Number(y))
                    }
                    
                })
                
            })
            it("check sorting node-id desc",function(){
                NodesPage.Visit()
                
                cy.get('.v-data-footer__select > .v-input > .v-input__control > .v-input__slot > .v-select__slot > .v-input__append-inner > .v-input__icon > .v-icon').type("a{enter}")
                cy.xpath('//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[1]/table/thead/tr/th[1]/i').click()
    
                let x=1
                let y=1
                console.log(x)
                console.log(y)
                cy.wait(200)
            
                cy.get('tbody > :nth-child(1) > .text-start')
        
                cy
                    .get('.text-start').should('be.visible')
                    .eq(1)
                    .should('have.text','49')
        
                cy
                    .get('.text-start')
                    .then( items =>
                        {
                        
                        for (let i = 1; i < (items.length-1); i++) {
    
                            y=Number(items[i+1].innerText)
                            x=Number(items[i].innerText)
    
                            expect(Number(x)).to.be.greaterThan(Number(y))
                        }
                        
                    })
                    
                })
    });
    