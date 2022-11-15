$(document).ready(function(){

    // Product Variation
	$(".choose-size").hide();

	// Show size according to selected color
	$(".choose-color").on('click',function(){
		$(".choose-size").removeClass('active');
		$(".choose-size").removeClass('prod-id');
		$(".choose-color").removeClass('color-title');


		// $(".choose-color").removeClass('focused');
		// $(this).addClass('focused');

		var _color=$(this).attr('data-color');
		var _color_name=$(this).attr('color');

		// var _size=$('.choose-size').attr('data-size');
		console.log(_color+" color")
		console.log(_color_name+" cn")

		$(".choose-size").hide();
		$(".color"+_color).show();
		$(".color-"+_color).addClass('color-title');

		// $(".color"+_color).first().addClass('active');

		

	});
	// End

	// get product id
	$(".choose-size").on('click',function(){

		var _pId=$(this).attr('prod-id');


		$(".choose-size").removeClass('active');
		$(".choose-size").removeClass('prod-id');

		$(".size"+_pId).addClass('active');
		$(".size"+_pId).addClass('prod-id');

		console.log(_pId+'prod-id')

		// $(".choose-size").hide();
		// $(".color"+_color).show();
		// $(".color"+_color).first().addClass('active');

		

	});
	//end
    // Show the first selected color
	$(".choose-color").first().addClass('focused');
	var _color=$(".choose-color").first().attr('data-color');
	var _price=$(".choose-size").first().attr('data-price');

	$(".color"+_color).show();
	// $(".color"+_color).first().addClass('active');
	// $(".product-price").text(_price);


	// place order with razorpay


});