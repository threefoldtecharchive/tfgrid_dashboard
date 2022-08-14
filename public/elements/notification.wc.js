!function(){"use strict";function t(){}function e(t){return t()}function n(){return Object.create(null)}function o(t){t.forEach(e)}function r(t){return"function"==typeof t}function s(t,e){return t!=t?e==e:t!==e||t&&"object"==typeof t||"function"==typeof t}function c(e,n,o){e.$$.on_destroy.push(function(e,...n){if(null==e)return t;const o=e.subscribe(...n);return o.unsubscribe?()=>o.unsubscribe():o}(n,o))}function i(t,e,n){t.insertBefore(e,n||null)}function l(t){t.parentNode.removeChild(t)}function u(t){return document.createElement(t)}function a(t){return document.createTextNode(t)}function f(t,e,n){null==n?t.removeAttribute(e):t.getAttribute(e)!==n&&t.setAttribute(e,n)}function d(t){const e={};for(const n of t)e[n.name]=n.value;return e}let p;function h(t){p=t}const m=[],$=[],g=[],y=[],b=Promise.resolve();let _=!1;function x(t){g.push(t)}let w=!1;const k=new Set;function v(){if(!w){w=!0;do{for(let t=0;t<m.length;t+=1){const e=m[t];h(e),E(e.$$)}for(h(null),m.length=0;$.length;)$.pop()();for(let t=0;t<g.length;t+=1){const e=g[t];k.has(e)||(k.add(e),e())}g.length=0}while(m.length);for(;y.length;)y.pop()();_=!1,w=!1,k.clear()}}function E(t){if(null!==t.fragment){t.update(),o(t.before_update);const e=t.dirty;t.dirty=[-1],t.fragment&&t.fragment.p(t.ctx,e),t.after_update.forEach(x)}}const M=new Set;let T,H;function L(t,e){t&&t.i&&(M.delete(t),t.i(e))}function C(t,e,n,o){if(t&&t.o){if(M.has(t))return;M.add(t),T.c.push((()=>{M.delete(t),o&&(n&&t.d(1),o())})),t.o(e)}}function j(t,n,s,c){const{fragment:i,on_mount:l,on_destroy:u,after_update:a}=t.$$;i&&i.m(n,s),c||x((()=>{const n=l.map(e).filter(r);u?u.push(...n):o(n),t.$$.on_mount=[]})),a.forEach(x)}function A(t,e){const n=t.$$;null!==n.fragment&&(o(n.on_destroy),n.fragment&&n.fragment.d(e),n.on_destroy=n.fragment=null,n.ctx=[])}function N(t,e){-1===t.$$.dirty[0]&&(m.push(t),_||(_=!0,b.then(v)),t.$$.dirty.fill(0)),t.$$.dirty[e/31|0]|=1<<e%31}function R(e,r,s,c,i,u,a,f=[-1]){const d=p;h(e);const m=e.$$={fragment:null,ctx:null,props:u,update:t,not_equal:i,bound:n(),on_mount:[],on_destroy:[],on_disconnect:[],before_update:[],after_update:[],context:new Map(r.context||(d?d.$$.context:[])),callbacks:n(),dirty:f,skip_bound:!1,root:r.target||d.$$.root};a&&a(m.root);let $=!1;if(m.ctx=s?s(e,r.props||{},((t,n,...o)=>{const r=o.length?o[0]:n;return m.ctx&&i(m.ctx[t],m.ctx[t]=r)&&(!m.skip_bound&&m.bound[t]&&m.bound[t](r),$&&N(e,t)),n})):[],m.update(),$=!0,o(m.before_update),m.fragment=!!c&&c(m.ctx),r.target){if(r.hydrate){const t=function(t){return Array.from(t.childNodes)}(r.target);m.fragment&&m.fragment.l(t),t.forEach(l)}else m.fragment&&m.fragment.c();r.intro&&L(e.$$.fragment),j(e,r.target,r.anchor,r.customElement),v()}h(d)}function S(t){let e,n;return{c(){e=u("div"),f(e,"class","notification"),f(e,"style",n=`background-color: ${Y(t[0])}; color: white`)},m(n,o){i(n,e,o),e.innerHTML=t[1]},p(t,o){2&o&&(e.innerHTML=t[1]),1&o&&n!==(n=`background-color: ${Y(t[0])}; color: white`)&&f(e,"style",n)},d(t){t&&l(e)}}}function O(t){let e;return{c(){e=u("div"),f(e,"class","notification"),f(e,"style","background-color: #fffaeb; color: #946c00")},m(n,o){i(n,e,o),e.innerHTML=t[1]},p(t,n){2&n&&(e.innerHTML=t[1])},d(t){t&&l(e)}}}function B(t){let e;return{c(){e=u("div"),f(e,"class","notification"),f(e,"style","background-color: transparent; color: #333")},m(n,o){i(n,e,o),e.innerHTML=t[1]},p(t,n){2&n&&(e.innerHTML=t[1])},d(t){t&&l(e)}}}function F(t){let e,n,o,r;return{c(){e=u("div"),n=a("Your solution is now starting. Please be patient"),f(e,"class",o="notification"),f(e,"style",r=`background-color: ${Y(t[0])}; color: white`)},m(t,o){i(t,e,o),function(t,e){t.appendChild(e)}(e,n)},p(t,n){1&n&&r!==(r=`background-color: ${Y(t[0])}; color: white`)&&f(e,"style",r)},d(t){t&&l(e)}}}function P(e){let n,o;function r(t,e){return"gray"==t[0]?B:"warning"==t[0]?O:S}let s=r(e),c=s(e),u=e[2]&&F(e);return{c(){c.c(),n=a(" "),u&&u.c(),o=a(""),this.c=t},m(t,e){c.m(t,e),i(t,n,e),u&&u.m(t,e),i(t,o,e)},p(t,[e]){s===(s=r(t))&&c?c.p(t,e):(c.d(1),c=s(t),c&&(c.c(),c.m(n.parentNode,n))),t[2]?u?u.p(t,e):(u=F(t),u.c(),u.m(o.parentNode,o)):u&&(u.d(1),u=null)},i:t,o:t,d(t){c.d(t),t&&l(n),u&&u.d(t),t&&l(o)}}}function Y(t){switch(t){case"info":case"success":return"#1982b1";case"danger":return"#FF5151";default:return""}}function q(t,e,n){let{type:o}=e,{message:r}=e,{deployed:s=!1}=e;return t.$$set=t=>{"type"in t&&n(0,o=t.type),"message"in t&&n(1,r=t.message),"deployed"in t&&n(2,s=t.deployed)},[o,r,s]}"function"==typeof HTMLElement&&(H=class extends HTMLElement{constructor(){super(),this.attachShadow({mode:"open"})}connectedCallback(){const{on_mount:t}=this.$$;this.$$.on_disconnect=t.map(e).filter(r);for(const t in this.$$.slotted)this.appendChild(this.$$.slotted[t])}attributeChangedCallback(t,e,n){this[t]=n}disconnectedCallback(){o(this.$$.on_disconnect)}$destroy(){A(this,1),this.$destroy=t}$on(t,e){const n=this.$$.callbacks[t]||(this.$$.callbacks[t]=[]);return n.push(e),()=>{const t=n.indexOf(e);-1!==t&&n.splice(t,1)}}$set(t){var e;this.$$set&&(e=t,0!==Object.keys(e).length)&&(this.$$.skip_bound=!0,this.$$set(t),this.$$.skip_bound=!1)}});class z extends H{constructor(t){super(),this.shadowRoot.innerHTML='<style>@import url("https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css");</style>',R(this,{target:this.shadowRoot,props:d(this.attributes),customElement:!0},q,P,s,{type:0,message:1,deployed:2},null),t&&(t.target&&i(t.target,this,t.anchor),t.props&&(this.$set(t.props),v()))}static get observedAttributes(){return["type","message","deployed"]}get type(){return this.$$.ctx[0]}set type(t){this.$$set({type:t}),v()}get message(){return this.$$.ctx[1]}set message(t){this.$$set({message:t}),v()}get deployed(){return this.$$.ctx[2]}set deployed(t){this.$$set({deployed:t}),v()}}function D(t,e,n){const o=t.slice();return o[3]=e[n].type,o[4]=e[n].message,o}function G(t){let e,n;return e=new z({props:{type:t[3],message:t[4]}}),{c(){var t;(t=e.$$.fragment)&&t.c()},m(t,o){j(e,t,o),n=!0},p(t,n){const o={};1&n&&(o.type=t[3]),1&n&&(o.message=t[4]),e.$set(o)},i(t){n||(L(e.$$.fragment,t),n=!0)},o(t){C(e.$$.fragment,t),n=!1},d(t){A(e,t)}}}function I(e){let n,r,s=e[0].notifications,c=[];for(let t=0;t<s.length;t+=1)c[t]=G(D(e,s,t));const a=t=>C(c[t],1,1,(()=>{c[t]=null}));return{c(){n=u("section");for(let t=0;t<c.length;t+=1)c[t].c();this.c=t,f(n,"class","notification-container")},m(t,e){i(t,n,e);for(let t=0;t<c.length;t+=1)c[t].m(n,null);r=!0},p(t,[e]){if(1&e){let r;for(s=t[0].notifications,r=0;r<s.length;r+=1){const o=D(t,s,r);c[r]?(c[r].p(o,e),L(c[r],1)):(c[r]=G(o),c[r].c(),L(c[r],1),c[r].m(n,null))}for(T={r:0,c:[],p:T},r=s.length;r<c.length;r+=1)a(r);T.r||o(T.c),T=T.p}},i(t){if(!r){for(let t=0;t<s.length;t+=1)L(c[t]);r=!0}},o(t){c=c.filter(Boolean);for(let t=0;t<c.length;t+=1)C(c[t]);r=!1},d(t){t&&l(n),function(t,e){for(let n=0;n<t.length;n+=1)t[n]&&t[n].d(e)}(c,t)}}}function J(t,e,n){let o;var r;const s=null===(r=window.configs)||void 0===r?void 0:r.notificationStore;return c(t,s,(t=>n(0,o=t))),[o,s]}customElements.define("tf-alert",z);customElements.define("tf-notification",class extends H{constructor(t){super(),this.shadowRoot.innerHTML='<style>@import url("https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css");.notification-container{z-index:9999;position:fixed;bottom:0;left:50%;transform:translateY(-50%);width:300px}</style>',R(this,{target:this.shadowRoot,props:d(this.attributes),customElement:!0},J,I,s,{},null),t&&t.target&&i(t.target,this,t.anchor)}})}();
