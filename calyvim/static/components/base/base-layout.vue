<script setup>
import { ConfigProvider } from 'ant-design-vue';

const theme = {
  token: {
    borderRadius: 5,
    colorPrimary: '#7D52E9',
    fontFamily: 'Nunito, sans-serif',
  },
}
</script>

<template>
  <ConfigProvider :theme="theme">
    <slot></slot>
  </ConfigProvider>
</template>