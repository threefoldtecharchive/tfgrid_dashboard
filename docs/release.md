# Releasing process

To create a new release there are some steps is required:

## 1. Update Charts file

In [charts.yaml](../charts/tfgrid-dashboard/Chart.yaml) replace the value of `appVersion` with the new release tag.

> NOTE: You can release or prerelease on ANY network. No tags are needed for releases & use x.x.x-rcx for prereleases.

```yaml
appVersion: "x.x.x"
```

## 2. **Create a new release**

Create a new release with same value of `appVersion` in `charts.yaml`.<br>
While you're creating a new release you also have to create a new tag the same as the one in the `charts.yaml`

> You can find more details about creating a new release in [Release projects](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release).

## 3. **Create a new issue on [tf_operations](https://github.com/threefoldtech/tf_operations)**

Create a new issue of type `Update Request` and mention the following:

- **Release link**

  You can find it by changing the branch to the needed tag and then copy the URL.

- **Charts directory link**

  In this case will be [dashboard-chart](../charts/tfgrid-dashboard/)

Newly created issue should look like this:

![image](https://user-images.githubusercontent.com/40770501/214016988-96a378a6-cb8b-4e15-aeb2-2c44576f9133.png)
