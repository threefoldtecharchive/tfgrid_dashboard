# How to get started

## To Run The Project follow these steps :

- clone the Repository : `git clone https://github.com/threefoldtech/tfgrid_dashboard.git`
- navigate to the Repository : `cd tfgrid_dashboard`
- make your on branch : `git checkout -b development_<FEATURE_NAME>`
- install the dependencies : `yarn install`
- run the project : `yarn run`
- open your browser and navigate to http://localhost:3000/
- Adjust your config.js file as per your environment::

  ```
  export GQL_URL="https://graphql.test.grid.tf/graphql"
  cd public
  source ../scripts/build-env.sh
  ```

## Architecture

### src

```
.
├── assets
├── Dashboard.vue
├── explorer
├── hub
├── main.ts
├── plugins
├── portal
├── router
├── shims-png.d.ts
├── shims-tsx.d.ts
├── shims-vue.d.ts
├── shims-vuetify.d.ts
└── store
```

#### Assets

- to add images to the project go to the assets folder and add the images you want to use in your project
- to add global styles to the project go to the assets folder then to the css folder and add the styles you want to use in your project

#### router

##### What is the purpose of the router?

- the router is the main component of the project it is responsible for routing the user to the right component
- the router can have nested routes to navigate to different components

##### How to use the router?

- simply import the component that you want to route to
- then append it to the routes array in this form :
  ```
  {
    component: <Component.>,
    path: "/<path>",
    children: <Nested-Router>,
  }
  ```
- If you want to create new Category in the sidebar then you need to create a new component and add it to the router

#### If you want to create new Category in the sidebar

- you create a new folder with the name of the category and inside it components,router (these will be the nested routes),Assets,lib (for manipulative functions) folder
- example :

```
.
├── assets
├── components
├── config.ts
├── Explorer.vue
├── filters
├── graphql
├── json
├── plugins
├── router
├── store
├── types
├── utils
└── views
```


