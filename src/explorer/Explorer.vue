<template>
  <v-container>
    <router-view />
    {{ $store.state.explorer.name }}
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Recusandae quidem asperiores ipsam aperiam quis ea illo quo odio repellendus? Praesentium atque neque nobis necessitatibus. Excepturi expedita reiciendis illo aperiam molestias.
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Ut repellendus aliquid aspernatur nihil distinctio reiciendis, voluptatibus deserunt recusandae nesciunt, odio debitis nemo provident mollitia quam vel qui impedit, facere itaque.
    Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quo, repudiandae sequi, ad aspernatur sunt, laborum molestiae quae nostrum eius nam reiciendis aut modi laboriosam magni provident? Officiis ullam ipsum provident!
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptas, tempora, doloribus assumenda laboriosam possimus illo necessitatibus cumque quisquam nobis aperiam deleniti, ea soluta quibusdam ut commodi eius culpa labore quae.
    Lorem ipsum, dolor sit amet consectetur adipisicing elit. Corporis labore odit molestias laborum pariatur magni non ea inventore id reiciendis tempora doloremque quaerat, provident cumque vel atque. Eaque, perspiciatis repellendus!Loremloree
    Lorem ipsum dolor, sit amet consectetur adipisicing elit. Amet dolores, excepturi esse earum beatae temporibus possimus consectetur laudantium dolore in accusantium voluptatum cumque quisquam quidem fugit ex ullam ad nisi.
    Lorem ipsum dolor sit amet, consectetur adipisicing elit. Perspiciatis ipsam, itaque ducimus explicabo similique alias. Nulla velit facere laudantium doloremque assumenda aut odit modi quaerat, quod quisquam quia nesciunt sequi?
    Lorem ipsum dolor sit, amet consectetur adipisicing elit. Odio, eaque exercitationem porro quis tempora corrupti consequuntur? Reiciendis voluptatum ratione quo laboriosam, numquam et expedita consequuntur atque dolor sed aliquam ullam?

  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  name: "ExplorerView",
})
export default class ExplorerView extends Vue {}
</script>
