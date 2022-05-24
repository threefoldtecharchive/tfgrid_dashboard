export async function getFarm (api: any, twinID:number) {
    const farms = await api.query.tfgridModule.farms.entries()
    const twinFarms = farms.filter((farm: { toJSON: () => { (): any; new(): any; twin_id: number } }[]) => {
      if (farm[1].toJSON().twin_id === twinID) {
        return farm
      }
    })
  
   
  
    return await twinFarms
  }