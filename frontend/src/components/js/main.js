$(function () {
	// INITIALIZE DATEPICKER PLUGIN
	$('.datepicker').datepicker({
		clearBtn: true,
		autoclose: true,
		format: "yyyy-mm-dd"
	});

	$('#timepicker').timepicker({
        template: 'dropdown',
        showInputs: false,
        minuteStep: 60,
        showMeridian: false,
		defaultTime: 'current',
		disableMousewheel: true,
		autoclose: true, 
		icons: {                  
			up: 'fa fa-chevron-up',
			down: 'fa fa-chevron-down'
		},
    });

	// 시간이 선택되면 값을 인풋에 설정
	$('#timepicker').on('changeTime.timepicker', function (e) {
		var pickedTime = e.time.value;
		$('#timepicker input').val(pickedTime);
	});

	

});


