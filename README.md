## THREEFOLD GRID DASHBOARD

A unified application where users can do the following and so much more !

- View and search their connected polkadot.js accounts
- Connect/Disconnect from polkadot.js
- View balances on the TF Chain
- Buy TFT
- Transfer TFT within the TFChain
- Swap TFT to and from Cosmos and Stellar 
- Create/delete/edit/view/search twins, farms, farm public IPs, farm nodes and farm nodes public        configuration. 
- Add Stellar payout to farms
- Reserve/Unreserve dedicated nodes. 
- Explore the grid capacity (i.e view the TF Grid statistics, nodes and farms across the world). 

If you don't know where to start, you can also review the TF Chain manual before even connecting to polkadot.js. 

### Built With
- Vue 2
- Typescript
- Veutify
- GraphQl

### Getting Started
To get a local copy up and running follow these simple example steps:
- Open Terminal.
- Change the current working directory to the location you want the cloned directory.
- Enter the following:
```
git clone https://github.com/threefoldtech/tfgrid_dashboard.git
```
- Press Enter to create your local clone.

- Navigate to the cloned repository by running:
```
cd tfgrid_dashboard
```

Adjust your config.js file as per your environment:

```bash
export GQL_URL="https://graphql.test.grid.tf/graphql"
cd public
source ../scripts/build-env.sh
```

To Try the project locally you can easy clone the repo and run the following commands:

```bash
yarn install
yarn serve
```

### Prerequisites:
- GitHub
- Git
- Node.js
- Yarn
- Vue CLI


### Contributors
Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](https://github.com/threefoldtech/tfgrid_dashboard/issues).
