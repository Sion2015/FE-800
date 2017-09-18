## **jFormslider v1.1.0** ##

jFormslider v1.1.0 is a jquery pluggin where we can convert a big form in to a slider
Form should be in ul li format

[Website](http://jformslider.com)
[Demo](http://jformslider.com/#demo)
[Docs](http://jformslider.com/docs)
```
<div id="slider">
	<ul>
		<li>--form componants--</li>
		<li>--form componants--</li>
		<li>--form componants--</li>
	</ul>
</div>
```
## **Usage** ##
```
//default options
options={
var options={
            width:600,
            height:300,
            movement:'horizontal',
            next_button:true,
            prev_button:true,
            button_placement:'bottom',
            submit_button:true,
            submit_class:'',
            next_class:'',
            prev_class:'',
            error_class:'error',
            input_error_class:'',
            error_element:'p',
            texts:{
                    next:'next',
                    prev:'prev',
                    submit:'submit'
                  },
            speed:400,
            submit_handler:function(){},
            slide_on_url:false,
			slide_effect:true,
			responsive_widths:[
				{range:[0,360],width:"30%"},
				{range:[361,640],width:"50%"},
				{range:[641,767],width:"65%"},
				{range:[768,991],width:"75%"},
				{range:[992,1199],width:"100%"}
			]
        }	
	$('#slider').jFormslider(options);//usage
```

## **Features** ##
## **Little validations**##
if you want to validate a input or select element put attribute 'required' and to overide default message put attribute 'data-msg'

```

ex:<input type="text" name="username" required data-msg="Please enter username"/>
```

if you want to validate email put attribute 'email'

```
#!html

ex:<input type="text" name="email" required data-msg="Please enter a valid email "/>
```

## **Call before** ##

Before sliding to next slide you can call a function For this just put attribute

```
data-callbefore="some_function()" 
```

in li Before loading this li it will call this function function should return true if you want to slide to this li function should return false if you dont want to slide to this li

## **Goto slide** ##
If you want to goto particular li without clicking through all slides you can call

```
$('#slider').gotoSlide(data-id)
```

you should specify a attribute in li called 'data-id' for this

```

<li data-id="middle_page"></li>
$('#slider').gotoSlide('middle_page')
```
For more options and docs visit [jformslider.com](http://jformslider.com/)

Please report bugs to bugs@jformslider.com
