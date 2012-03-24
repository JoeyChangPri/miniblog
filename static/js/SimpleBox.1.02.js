/*
 * SimpleBox.js plugin
 * Copyright (c) 2009, Marcin Rosinski. (http://www.simpletags.org/)
 * All rights reserved.
 * 
 * LICENCE
 *
 * Redistribution and use in source and binary forms, with or without modification, 
 * are permitted provided that the following conditions are met:
 *
 * - 	Redistributions of source code must retain the above copyright notice, 
 * 		this list of conditions and the following disclaimer.
 * 
 * -	Redistributions in binary form must reproduce the above copyright notice, 
 * 		this list of conditions and the following disclaimer in the documentation and/or other 
 * 		materials provided with the distribution.
 * 
 * -	Neither the name of the Simpletags.org nor the names of its contributors may be used to 
 * 		endorse or promote products derived from this software without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR 
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY 
 * AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR 
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER 
 * IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF 
 * THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * 
 * @script    		SimpleBox.js
 * @description		jQuery content overlay plugin
 * @copyright  		Copyright (c) 2009 Marcin Rosinski. (http://www.simpletags.org/)
 * @license    		http://www.simpletags.org/simpletools/licence	(BSD)
 * @version    		Ver: 1.02 2009-10-27 17:43
 * 
 */

var SimpleBox = {
		
	__init: false,
	
	__settings : {
		directInput:false,
		exitOnEsc:true,
		showCloseImage:false,
		closeImageCss: {'z-index':'3'},
		defaultCloseImageSrc: '',
		hoverCloseImageSrc: '',
		showCaption: false,
		captionText: '',
		captionCss: {},
		overlayBackground: '#000',
		overlayOpacity: 0.75,
		webKitRoundCorners: false,
		openingSpeed: 200,
		closingSpeed: 200,
		clone: false,
		onClose: false,
		onCloseParam: null,
		onOpen: false,
		onOpenParam: null,
		globalCss: false
	},
	
	__scroll_top : 0,
	__input_name : false,
	__esc_listener : false,
	
	__overlay_css : {},
	__container_css : {},
	
	__body_css : {},
	__head_css:	{},	
	
	getDefaultCssValues: function(name)
	{
		switch(name)
		{
			case 'body':
				return {'color':'#333','background':'#fff','padding':'10px','position':'relative','display':'block','clear':'both'};
			case 'head':
				return {'position':'absolute','display':'block','background':'transparent','width':'100px','height':'40px','color':'#fff','top':'-30px'};
			case 'captionCss':
				return {'position':'absolute','left':'0','top':'10px','padding':'0 0 0 5px','color':'#fff','margin':'0','font-size':'14px'};
			case 'overlay':
				return {'display':'none','position':'fixed','top':'0','left':'0','z-index':'100000000','width':'100%','height':'100%','background':'#000','opacity':0.75};
			case 'container':
				return {'display':'none','color':'#333','background':'transparent','padding':'0','position':'fixed','top':'50%','left':'50%','z-index':'100000001'};
			default:
				return {};
		}
	},
	
	open: function(input,settings)
	{	
		if(!this.__settings.globalCss || !this.__init)
		{
			this.__body_css 			= this.getDefaultCssValues('body');
			this.__head_css 			= this.getDefaultCssValues('head');
			this.__settings.captionCss 	= this.getDefaultCssValues('captionCss');
			this.__overlay_css			= this.getDefaultCssValues('overlay');
			this.__container_css		= this.getDefaultCssValues('container');
		}
		
		if(settings.hasOwnProperty('fbStyle'))
		{
			this.__settings.overlayBackground = '#000';
			this.__settings.overlayOpacity = 0;
			this.__container_css.padding = 12;
			if(settings.fbStyle.hasOwnProperty('borderColor')) 
				this.__container_css.background = settings.fbStyle.borderColor
			else 
				this.__container_css.background = '#2e2e2e';
			
			this.addWebKitRoundCornersContainer();
			
			this.__settings.bodyWebKitRoundCorners = 2;
			this.addWebKitRoundCorners();
		}
		
		this.__init = true;
		
		this.__settings.directInput = false;
		
		if(!settings.onClose) this.__settings.onClose = false;
		if(!settings.onOpen) this.__settings.onOpen = false;
			
		if(settings.captionCss) 
		{
			jQuery.extend(this.__settings.captionCss,settings.captionCss);
			delete settings.captionCss;
		}
		
		if(settings.closeImageCss)
		{
			jQuery.extend(this.__settings.closeImageCss,settings.closeImageCss);
			delete settings.closeImageCss;
		}
		
		if(settings.bodyCss) jQuery.extend(this.__body_css,settings.bodyCss);
		if(settings.headCss) jQuery.extend(this.__head_css,settings.headCss);
		
		if(settings) jQuery.extend(this.__settings,settings);
		
		this.__overlay_css.background = this.__settings.overlayBackground;
		this.__overlay_css.opacity = this.__settings.overlayOpacity;
		
		if(!this.__esc_listener) 
		{
			if(this.__settings.exitOnEsc) jQuery(document).keyup(function(event){if (event.keyCode == 27) {SimpleBox.close();}});
			this.__esc_listener = true;
		}
		
		if(this.__settings.bodyWebKitRoundCorners)
		{
			this.addWebKitRoundCorners();
		}
		
		if(jQuery.browser.msie && jQuery.browser.version.substr(0,1) < 7) 
		{
			this.__container_css.position = 'absolute';
			this.__overlay_css.position = 'absolute';
			this.__overlay_css.height = jQuery(document).height()+'px';
		}
		
		this.appendToBody();
		this.insert(input);
		this.show();
	},
	
	init: function()
	{
		if(!this.__init)
		{
			this.__init_copy.settings = this.__settings
			this.__init = true;
		}
	},
	
	addWebKitRoundCorners: function()
	{
		corners = {'border-radius':this.__settings.bodyWebKitRoundCorners+'px','-moz-border-radius':this.__settings.bodyWebKitRoundCorners+'px','webkit-border-radius':this.__settings.bodyWebKitRoundCorners+'px'};
		jQuery.extend(this.__body_css,corners);
	},
	
	addWebKitRoundCornersContainer: function()
	{
		corners = {'border-radius':'5px','-moz-border-radius':'5px','webkit-border-radius':'5px'};
		jQuery.extend(this.__container_css,corners);
	},
	
	addCloseButton: function()
	{
		jQuery("#SimpleBox_head").append('<img id="SimpleBox_closeButton" src="'+this.__settings.defaultCloseImageSrc+'" style="cursor: pointer; position: absolute; right: -3px; top: 5px;" title="close" alt="close" />');
		
		jQuery("#SimpleBox_closeButton").css(this.__settings.closeImageCss);
		
		if(this.__settings.hoverCloseImageSrc)
		{
			jQuery("#SimpleBox_closeButton").mouseover(function(){
				jQuery(this).attr('src',SimpleBox.__settings.hoverCloseImageSrc);
			});
			jQuery("#SimpleBox_closeButton").mouseout(function(){
				jQuery(this).attr('src',SimpleBox.__settings.defaultCloseImageSrc);
			});
		}
		
		jQuery("#SimpleBox_closeButton").click(function(){SimpleBox.close()});
	},
	
	addCaption: function()
	{
		jQuery("#SimpleBox_head").append('<h3 id="SimpleBox_caption" style="position: absolute; left: 0px; top: 0px;">'+this.__settings.captionText+'</h3>');
		jQuery("#SimpleBox_caption").css(this.__settings.captionCss);
	},
	
	insert: function(input)
	{
		
		if(this.__settings.showCloseImage && this.__settings.showCaption)
		{
			this.addCloseButton();
			this.addCaption();
		}
		else if(this.__settings.showCloseImage && !this.__settings.showCaption)
			this.addCloseButton();
		else if(!this.__settings.showCloseImage && this.__settings.showCaption)
			this.addCaption();
		
		if(!this.__settings.directInput) 
		{
			jQuery("#SimpleBox_body").append(jQuery(input).html());
			
			//for cloning purposes
			if(!this.__settings.clone)
			{
				jQuery(input).html('');
				this.__input_name = input;
			}
		}
		else jQuery("#SimpleBox_body").html(input);
		
	},
	
	appendToBody: function()
	{
		jQuery('body').append('<div id="SimpleBox_overlay" style="display: none;"></div><div id="SimpleBox_container" style="display: none;"><div id="SimpleBox_head" style="position: relative"></div><div id="SimpleBox_body" style="position: relative"></div></div>');
		
		jQuery('#SimpleBox_overlay').css(this.__overlay_css);
		jQuery('#SimpleBox_container').css(this.__container_css);
		
		jQuery('#SimpleBox_head').css(this.__head_css);
		jQuery('#SimpleBox_body').css(this.__body_css);

		jQuery('#SimpleBox_overlay').click(function(){
			SimpleBox.close();
		});
	},
	
	show: function()
	{
		jQuery("#SimpleBox_overlay").fadeIn(this.__settings.openingSpeed,function(){
			if(SimpleBox.__settings.onOpen) SimpleBox.__settings.onOpen(SimpleBox.__settings.onOpenParam);
		});
		
		SimpleBox_container_css = {'marginLeft':'-'+(jQuery("#SimpleBox_container").width()/2)+'px'};
		SimpleBox_container_css.marginTop = '-'+(jQuery("#SimpleBox_container").height()/2)+'px';
			
		
		if(jQuery('body').innerHeight() < jQuery("#SimpleBox_container").height())
		{
			SimpleBox_container_css.marginTop 	= '4%';
			SimpleBox_container_css.top			= 0;
		}
			
		jQuery("#SimpleBox_container").css(SimpleBox_container_css);
		
		jQuery("#SimpleBox_head").css('width',jQuery("#SimpleBox_container").width()+'px');
		
		startHeight = jQuery("#SimpleBox_container").height();
		jQuery("#SimpleBox_body").height(startHeight)
		finalHeightDiff = jQuery("#SimpleBox_container").height() - startHeight;
		jQuery("#SimpleBox_body").height(startHeight-finalHeightDiff);
		
		this.__scroll_top = jQuery('html').scrollTop();
		jQuery("#SimpleBox_container").fadeIn(this.__settings.openingSpeed);
	},
	
	close: function(callback,callbackParam)
	{
		jQuery('#SimpleBox_overlay').fadeOut(this.__settings.closingSpeed,function(){
			
			jQuery('#SimpleBox_head').remove();
			
			jQuery('#SimpleBox_overlay').remove();
			
			if(callback) callback(callbackParam);
			else if(SimpleBox.__settings.onClose) SimpleBox.__settings.onClose(SimpleBox.__settings.onCloseParam);
			
		});
		
		if(!SimpleBox.__settings.directInput && !SimpleBox.__settings.clone)
		{
			jQuery(SimpleBox.__input_name).html(jQuery('#SimpleBox_body').html());
		}
		jQuery('#SimpleBox_container').remove();
	}
		
}