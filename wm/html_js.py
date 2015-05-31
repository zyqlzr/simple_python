#!/usr/bin/python
# -*- coding=utf-8 -*-

submit_js = '''
var data = {};
var user_addr = {};
var submit_flag = false;
var ready_flag = false;
var total_price = 0;
var dc_price = 0;

$(document).ready(function() {
   var submit_dom = $('.submit');
   var addr_val = $('.info-addr').children('.info-value').html();
   var phone_val = $('.info-phone').children('.info-value').html();

   if (0 == addr_val.length || 0 == phone_val.length) {
       if (submit_dom.hasClass('checkmark_on')) {
           submit_dom.removeClass('checkmark_on');
       }

       if (!submit_dom.hasClass('checkmark')) {
           submit_dom.addClass('checkmark');
       }
       ready_flag = false;
   } else {
       if (submit_dom.hasClass('checkmark')) {
           submit_dom.removeClass('checkmark');
       }

       if (!submit_dom.hasClass('checkmark_on')) {
           submit_dom.addClass('checkmark_on');
       }
       ready_flag = true;
   }

   var dc_dom = $('.discount');
   var dc_type = dc_dom.data('type');
   var dc_title = dc_dom.data('title');

   var ul_dom = $('.order-list');
   var order_dom = $('.fyy-order');
   var menu = LS.get('orders', true);
   var price = parseInt(LS.get('price', false));
   for (mid in menu) {
       var ele = menu[mid];
       if (('num' in ele) && ('title' in ele)) {
           var num = ele['num'] + " 份";
           li_dom = $("<li />", {text:ele['title']});
           li_dom.addClass('order-e');
           $("<strong />", {text: num}).appendTo(li_dom);
           li_dom.appendTo(ul_dom);
       }
   }

   total_price = price;
   var total_price_des = "总价";
   var discount_des = "优惠";
   if (0 == dc_type) {
   } else if (1 == dc_type) {
       dc_price = parseInt(price / 2);
       var left = price % 2;
       if (left > 0) {
           total_price = left + dc_price; 
       } else {
           total_price = dc_price;
       }
       total_price_des = "折后总价"

       var text_str = discount_des + dc_price + "￥";
       p_dc = $("<p />", {text:dc_title});
       p_dc.addClass('order-des');
       $("<strong />", {text:text_str}).appendTo(p_dc);
       p_dc.appendTo(order_dom);
   } else {
       p_dc = $("<p />", {text:discount_des});
       p_dc.addClass('order-des');
       $("<strong />", {text:dc_title}).appendTo(p_dc);
       p_dc.appendTo(order_dom);
   }

   var total_str = total_price + "￥";
   p_total = $("<p />", {text:total_price_des});
   p_total.addClass('order-des');
   $("<strong />", {text:total_str}).appendTo(p_total);
   p_total.appendTo(order_dom);
})


$('.submit').on('tap', function(){
    if (submit_flag) {
        return;
    }

    if (!ready_flag) {
        return;
    }
    submit_flag = true;

    var id_dom = $('.fyy-openid');
    var url_pre = "http://www.fanyoyo.cn/openid?submit=";
    var id = id_dom.html();
    var submit_url = url_pre + id;
    var menu = LS.get('orders', true);

    data['id'] = id;
    data['menu'] = menu;
    data['price'] = total_price;
    data['discount'] = dc_price;

    var s_data = JSON.stringify(data);
    var ok = "send ok,body=" + s_data;
    $.ajax({
        type: 'POST',
        url:submit_url,
        data: s_data,
        dataType:'json',
        timeout: 3000,
        success: function(data){
          location.href='http://www.fanyoyo.cn/wm_html/wm_fini.html';
        },
        error: function() {
          location.href='http://www.fanyoyo.cn/wm_html/wm_fail.html';
        }
    })
});


$('.addr-add').on('tap', function(){
    var addr_dom = $('.fyy-add');
    var add_dom = $('.addr-add');
    var ul_dom = $('.fyy-order');

    if (addr_dom.hasClass('hide')) {
        addr_dom.removeClass('hide');
    }

    if (!add_dom.hasClass('hide')) {
        add_dom.addClass('hide');
    }
})

$('.info-edit').on('tap', function(){
    var add_dom = $('.fyy-add');
    var info_dom = $('.fyy-info');
    var ul_dom = $('.fyy-order');

    if (add_dom.hasClass('hide')) {
        add_dom.removeClass('hide');
    }

    if (!info_dom.hasClass('hide')) {
        info_dom.addClass('hide');
    }

    if (!ul_dom.hasClass('hide')) {
        ul_dom.addClass('hide');
    }
})

$('.input-check').on('tap', function(){
    var submit_dom = $('.submit');
    var input_addr_dom = $('.input-addr');
    var input_phone_dom = $('.input-phone');

    var addr_dom = $('.fyy-add');
    var info_dom = $('.fyy-info');
    var ul_dom = $('.fyy-order');

    addr_val = input_addr_dom.val();
    phone_val = input_phone_dom.val();
    if (0 == addr_val.length  || phone_val.length != 11) {
        alert("请输入正确的地址和电话号码");
        return;
    }

    $('.info-addr').children('.info-value').html(addr_val);
    $('.info-phone').children('.info-value').html(phone_val);

    user_addr['type'] = 0;
    user_addr['addr'] = addr_val;
    user_addr['phone'] = phone_val;
    data['user_info'] = user_addr;

    if (!addr_dom.hasClass('hide')) {
        addr_dom.addClass('hide');
    }

    if (info_dom.hasClass('hide')) {
        info_dom.removeClass('hide');
    }

    if (ul_dom.hasClass('hide')) {
        ul_dom.removeClass('hide');
    }

    if (submit_dom.hasClass('checkmark')) {
        submit_dom.removeClass('checkmark');
    }

    if (!submit_dom.hasClass('checkmark_on')) {
        submit_dom.addClass('checkmark_on');
    }
    ready_flag = true;
})

'''

order_js = '''
var submit_dom = document.getElementById('submit');
var sel_num_dom = $('#count');
var money_num_dom = $('#money_num');

var flag_dom = $('.menu-flag');
var titles_dom = $('.menu-titles');
var dinner_base = '.fyy-dinner-';

var sel_num_counter = 0;
var money_num_counter = 0;
var orders = {};
var timeout_counter = null;
var down_up_flag = true;
var dinner_type = 0;

var _msg = function(dom, msg){
    var tip_dom = $(dom).parent().parent().find('.fyy-tt-tips');
    tip_dom.html(msg).removeClass('hide');
    if(timeout_counter!=null)clearTimeout(timeout_counter);
    timeout_counter = setTimeout(function(){tip_dom.addClass('hide')}, 1500);
}

var _show = function(){
    sel_num_dom.html(sel_num_counter+'份');
    money_num_dom.html(money_num_counter);
}

$(document).on('touchend', '.menu-title', function(){
    if (down_up_flag) {
        if (flag_dom.hasClass('up')) {
            flag_dom.removeClass('up');
        }
        if (!flag_dom.hasClass('down')) {
            flag_dom.addClass('down');
        }
        if (!titles_dom.hasClass('hide')) {
            titles_dom.addClass('hide');
        }
        down_up_flag = false;
    } else {
        if (flag_dom.hasClass('down')) {
            flag_dom.removeClass('down');
        }
        if (!flag_dom.hasClass('up')) {
            flag_dom.addClass('up');
        }
        if (titles_dom.hasClass('hide')) {
            titles_dom.removeClass('hide');
        }
        down_up_flag = true;
    }
})

$(document).on('touchend', '.ts', function() {
    title_type = $(this).data('type');
    if (dinner_type != title_type) {
        if (!$(this).hasClass('highlight')) {
            $(this).addClass('highlight');
        }
        xc_dom = $('.xc');
        yl_dom = $('.yl');
        if (xc_dom.hasClass('highlight')) {
            xc_dom.removeClass('highlight');
        }
        if (yl_dom.hasClass('highlight')) {
            yl_dom.removeClass('highlight');
        }
        old_dinner_attr = dinner_base + dinner_type;
        new_dinner_attr = dinner_base + title_type;
        dinner_type = title_type;
        old_dinner_dom = $(old_dinner_attr);
        new_dinner_dom = $(new_dinner_attr);
        if (!old_dinner_dom.hasClass('hide')) {
            old_dinner_dom.addClass('hide');
        }
        if (new_dinner_dom.hasClass('hide')) {
            new_dinner_dom.removeClass('hide');
        }
        
        title_name = $(this).html();
        name_dom = $('.menu-name');
        name_dom.html(title_name);
    }
})

$(document).on('touchend', '.xc', function() {
    title_type = $(this).data('type');
    if (dinner_type != title_type) {
        if (!$(this).hasClass('highlight')) {
            $(this).addClass('highlight');
        }
        yl_dom = $('.yl');
        ts_dom = $('.ts');
        if (yl_dom.hasClass('highlight')) {
            yl_dom.removeClass('highlight');
        }
        if (ts_dom.hasClass('highlight')) {
            ts_dom.removeClass('highlight');
        }
        old_dinner_attr = dinner_base + dinner_type;
        new_dinner_attr = dinner_base + title_type;
        dinner_type = title_type;
        old_dinner_dom = $(old_dinner_attr);
        new_dinner_dom = $(new_dinner_attr);
        if (!old_dinner_dom.hasClass('hide')) {
            old_dinner_dom.addClass('hide');
        }
        if (new_dinner_dom.hasClass('hide')) {
            new_dinner_dom.removeClass('hide');
        }

        title_name = $(this).html();
        name_dom = $('.menu-name');
        name_dom.html(title_name);
    }
})

$(document).on('touchend', '.yl', function() {
    title_type = $(this).data('type');
    if (dinner_type != title_type) {
        if (!$(this).hasClass('highlight')) {
            $(this).addClass('highlight');
        }
        xc_dom = $('.xc');
        ts_dom = $('.ts');
        if (xc_dom.hasClass('highlight')) {
            xc_dom.removeClass('highlight');
        }
        if (ts_dom.hasClass('highlight')) {
            ts_dom.removeClass('highlight');
        }
        old_dinner_attr = dinner_base + dinner_type;
        new_dinner_attr = dinner_base + title_type;
        dinner_type = title_type;
        old_dinner_dom = $(old_dinner_attr);
        new_dinner_dom = $(new_dinner_attr);
        if (!old_dinner_dom.hasClass('hide')) {
            old_dinner_dom.addClass('hide');
        }
        if (new_dinner_dom.hasClass('hide')) {
            new_dinner_dom.removeClass('hide');
        }

        title_name = $(this).html();
        name_dom = $('.menu-name');
        name_dom.html(title_name);
    }
})

$(document).on('touchend', '.minus', function(){
    var dom = $(this).next();
    if('0'==dom.html())return;
    var newnum = Number(dom.html()) - 1;
    var price = Number(dom.data('price'));
    var title = dom.data('title');

    if(newnum>=0){
        sel_num_counter--;
        money_num_counter -= price;
        _show();
    }

    if(newnum<=0){
        newnum=0;
    }
    
    if(sel_num_counter<=0){
        submit_dom.className = 'checkmark';
    }
    dom.html(newnum);
    orders[dom.data('food')] = {'num':newnum,  'title':title};;
});

$(document).on('touchend', '.plus', function(){
    var dom = $(this).prev();
    var newnum = Number(dom.html())+1;
    var price = Number(dom.data('price'));
    var title = dom.data('title');

    sel_num_counter++;
    money_num_counter += price;
    _show();
    submit_dom.className = 'checkmark_on';
    dom.html(newnum);
    orders[dom.data('food')] = {'num':newnum,  'title':title};
});

$('#submit').on('tap', function(){
    if(sel_num_counter<=0)return;
    var filtes = {};
    for (var i in orders) {
        var onum = orders[i]['num'];
        if (onum != 0) {
            filtes[i] = {'num': orders[i]['num'], 'title': orders[i]['title']};
        }
    }
    json = JSON.stringify(filtes);
    LS.set('orders', json);
    LS.set('price', money_num_counter);
    location.href = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx3de96fc1838e3116&redirect_uri=http://www.fanyoyo.cn/openid&response_type=code&scope=snsapi_base&state=1#wechat_redirect';
});

_show();
'''

