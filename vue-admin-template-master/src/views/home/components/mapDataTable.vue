<template>
    <div :style="styleObj">
        <Table :height="height" :columns="columns" :data="cityData"></Table>
    </div>
</template>

<script>
export default {
    name: 'mapDataTable',
    data() {
        return {
            columns: [
                {
                    title: '城市',
                    key: 'name',
                },
                {
                    title: '用户量',
                    key: 'value',
                    sortable: true,
                },
            ],
        }
    },
    props: {
        cityData: Array,
        styleObj: Object,
        height: String,
    },
}
</script>
