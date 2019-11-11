
    $(function() {
	setOption("echarts-1", {
		//标题
		title: {
			text: '年龄分布'
		},
		//工具栏
		tooltip: {},
		//图表图注
		legend: {
			data: ['人数']
		},
		//x轴
		xAxis: {
			data: ["18岁以下", "19-25岁", "26-35岁", "36-45岁", "46-55岁", "56岁以上", "未知"]
		},
		//y轴
		yAxis: {},
		//系列
		series: [{
			name: '人数',
			//图表类型设置
			type: 'bar',
    data: [0, 0, 1, 0, 0, 0, 0]				//年龄数据传入
    }]
	});
	setOption("echarts-2", {
		title: {
			text: '性别比例'
		},
		backgroundColor: '#3388cb',
		visualMap: {
			show: true,
			min: 0,
			max: 500000,
			inRange: {
				colorLightness: [2, 5.5]
			}
		},
		series: [{
			name: '性别比例',
			type: 'pie',
			radius: '60%',
			data: [{
    value: 1,	//性别数据传入
name: '男性',
}, {
value: 0,
name: '女性',
},{
value: 0,
name: '未知',
    }],
			roseType: 'angle',
			label: {
				normal: {
					textStyle: {
						color: 'rgba(255, 255, 255, 0.8)'
					}
				}
			},
			labelLine: {
				normal: {
					lineStyle: {
						color: 'rgba(255, 255, 255, 0.8)'
					}
				}
			},
			itemStyle: {
				normal: {
					color: '#c23531',
					// shadowBlur: 200,
					shadowColor: 'rgba(0, 0, 0, 0.8)'
				}
			}
		}]
	});
	setOption("echarts-3",{
	   title: {
    text: '2月会员注册人数统计'
    },
    tooltip: {
        trigger: 'axis'
    },
    // legend: {
    //     data:['上网','QQ','游戏','音乐','看电影']
    // },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name:'人数',
            type:'line',
            stack: '花费',
    data:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]       //总人数数据传入
    },
        // {
        //     name:'QQ',
        //     type:'line',
        //     stack: '花费',
        //     data:[220, 182, 191, 234, 290, 330, 310]
        // },
        // {
        //     name:'游戏',
        //     type:'line',
        //     stack: '花费',
        //     data:[150, 232, 201, 154, 190, 330, 410]
        // },
        // {
        //     name:'音乐',
        //     type:'line',
        //     stack: '花费',
        //     data:[320, 332, 301, 334, 390, 330, 320]
        // },
        // {
        //     name:'看电影',
        //     type:'line',
        //     stack: '花费',
        //     data:[820, 932, 901, 934, 1290, 1330, 1320]
        // }
    ]
	});
});
/*
 **功能:柱状、折线图
 **参数1：元素ID
 **参数2：配置项设置
 */
function setOption(ident, opt) {
	//基于准备好的dom,初始化echarts实例
	let myChart = echarts.init($('#' + ident)[0]);
	// 使用刚指定的配置项和数据显示图表。
	myChart.setOption(opt);
}
/*
 **功能:南丁格尔图
 **参数1：元素ID
 **参数2：配置项设置
 */
function setOption(ident, opt) {
	//基于准备好的dom,初始化echarts实例
	let myChart = echarts.init($('#' + ident)[0]);
	// 使用刚指定的配置项和数据显示图表。
	myChart.setOption(opt);
}
    