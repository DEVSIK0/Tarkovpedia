<script setup lang="ts">
import NavbarButton from "@/components/domain/navbar/NavbarButton.vue";

const router = useRouter();

const NAVBAR_BUTTONS = [
  {
    key: "navbar.bottom.profile",
    icon: "mdi:account-cog",
    disabled: false,
    position: "left",
    onCLick: () => {
      router.push("/profile");
    },
  },
  {
    key: "navbar.bottom.dashboard",
    icon: "meteor-icons:hexagon",
    disabled: true,
    position: "left",
    onCLick: () => {
      // router.push("/dashboard");
    },
  },
  {
    key: "navbar.bottom.maps",
    icon: "material-symbols:location-on",
    disabled: false,
    position: "left",
    onCLick: () => {
      router.push("/maps");
    },
  },
  {
    key: "navbar.bottom.items",
    icon: "material-symbols:shopping-cart",
    disabled: false,
    position: "left",
    onCLick: () => {
      router.push("/items");
    },
  },
  {
    key: "navbar.bottom.bug",
    icon: "material-symbols:bug-report",
    disabled: false,
    position: "right",
    onCLick: () => {
      window.open("https://github.com/DEVSIK0/Tarkovpedia/issues/new");
    },
  },
  {
    key: null,
    icon: "mdi:github",
    disabled: false,
    position: "right",
    onCLick: () => {
      window.open("https://github.com/DEVSIK0/Tarkovpedia");
    },
  },
];
</script>
<template>
  <nav class="flex justify-between p-1">
    <div class="buttons left">
      <NavbarButton :buttons="NAVBAR_BUTTONS.filter((b) => b.position === 'left')" />
    </div>
    <div class="buttons right">
      <NavbarButton :buttons="NAVBAR_BUTTONS.filter((b) => b.position === 'right')" />
    </div>
  </nav>
</template>

<style scoped>
nav {
  background-color: black;
  width: 100%;
  border-top: 1px solid hsla(0, 100%, 100%, 0.3);
  height: 44px;

  .buttons {
    display: flex;
    gap: 5px;
    padding: 0 5px;
  }
}
</style>
