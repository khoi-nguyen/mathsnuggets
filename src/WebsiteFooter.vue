<template lang="pug">
footer.footer
  .container.content
    .columns
      .column
        p #[b-icon(pack="far" icon="copyright")] #[strong MathsNuggets] by K. Nguyen and T. Chambaud (2020).
      .column.is-narrow
        dl.content
          dt License
          dd
            a(href="https://www.gnu.org/licenses/agpl-3.0.en.html") GNU AGPL v3
          dt Source code
          dd
            a(href="https://github.com/khoi-nguyen/mathsnuggets") Github repository
          dt Documentation
          dd
            a(href="/docs/") MathsNuggets
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
dt, strong {
  font-weight: 400;
}
</style>
