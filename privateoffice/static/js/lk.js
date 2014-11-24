$.ajaxSetup(
{
    beforeSend: function(xhr, settings)
    {
        function getCookie(name)
        {
            var cookieValue = null;
            if (document.cookie && document.cookie != '')
            {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++)
                {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '='))
                    {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url)))
        {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

function login(){
    LoginName = document.getElementById('id_login').value;
    LoginPassword = document.getElementById('id_password').value;
    query = {
        login:    LoginName,
        password: LoginPassword
    };
    $.ajax
    (
        {
            url:        "/login/",
            type:       "POST",
            data:       query,
            success:    function(data)
            {
                if (data == 'good')
                {
                    window.location.reload()
                }
                else
                {
                    alert(data)
                }
            }
        }

    )
}

function ShowLoginForm(){
    //alert(String.className);
    elem = document.getElementById('auth');
    if (elem.style.visibility == 'visible'){
        elem.style.visibility = 'hidden';
    }else{
        elem.style.visibility = 'visible';
    }

}

//var countryResultList = document.getElementById('searchCountry');
//var resortResultList = document.getElementById('searchResort');
//var hotelResultList = document.getElementById('searchHotel');
//countryResultList.style.backgroundColor = '#333';
//alert(hotelResultList.id)
var globString;
function searchGlobal(searchString)
{
    //if (searchString.value.length > 2)
    //{
        var countryResultList = document.getElementById('searchCountry');
        var resortResultList = document.getElementById('searchResort');
        var hotelResultList = document.getElementById('searchHotel');
        $.ajax
        (
            {
                url:        "/api/search/global/",
                type:       "POST",
                data:       searchString.value,
                success:    function(data)
                {
                    currentCountry = '';
                    globString = data;
                    //countryString = data['privateoffice.country']
                    //alert(hotelResultList.id)
                    while(countryResultList.lastChild) {countryResultList.removeChild(countryResultList.lastChild);}
                    while(resortResultList.lastChild) {resortResultList.removeChild(resortResultList.lastChild);}
                    while(hotelResultList.lastChild) {hotelResultList.removeChild(hotelResultList.lastChild);}
                    for (var i=0; i<globString.length; i++){
                        newdiv = document.createElement('div');
                        newdiv.className = 'searchElement';
                        if (globString[i].model == 'privateoffice.hotel')
                        {
                            newdiv.setAttribute('onclick', 'showParent(this)')
                            newdiv.id = "hotel_"+globString[i].pk
                            hotelResultList.insertBefore(newdiv, hotelResultList.firstChild);
                            newdiv.innerHTML = data[i].fields.name + '<span class="hotelPrice">$' + data[i].fields.price + '</span>';
                        }
                        else if (globString[i].model == 'privateoffice.resort')
                        {
                            newdiv.setAttribute('onclick', 'showOther(this)')
                            newdiv.id = "resort_"+globString[i].pk
                            resortResultList.insertBefore(newdiv, resortResultList.firstChild);
                            newdiv.innerHTML = globString[i].fields.name;
                        }
                        else
                        {
                            newdiv.setAttribute('onclick', 'showChildren(this)')
                            newdiv.id = "country_"+globString[i].pk
                            countryResultList.insertBefore(newdiv, countryResultList.firstChild);
                            newdiv.innerHTML = globString[i].fields.name;
                        }
                    }
                }
            }
        )
    //}
}
function showChildren(parent)
{
    var countryResultList = document.getElementById('searchCountry');
    var resortResultList = document.getElementById('searchResort');
    var hotelResultList = document.getElementById('searchHotel');
    if (currentCountry != ''){
        currentCountry.style.backgroundColor = '#fafafa';
    }
    currentCountry = parent
    parent.style.backgroundColor = selectedColor;
    parent_id = parent.id
    parent_pk = parent_id.substr(parent_id.indexOf('_') + 1)
    $.ajax
    (
        {
            url:        "/api/search/children/",
            type:       "POST",
            data:       parent_pk,
            success:    function(data)
            {
                while(resortResultList.lastChild) {resortResultList.removeChild(resortResultList.lastChild);}
                while(hotelResultList.lastChild) {hotelResultList.removeChild(hotelResultList.lastChild);}
                for (var i=0; i<data.length; i++)
                {
                    newdiv = document.createElement('div');
                    newdiv.className = 'searchElement';
                    if (data[i].model == 'privateoffice.hotel')
                    {
                        newdiv.setAttribute('onclick', 'showParent(this)')
                        newdiv.id = "hotel_"+data[i].pk
                        hotelResultList.insertBefore(newdiv, hotelResultList.firstChild);
                        newdiv.innerHTML = data[i].fields.name + '<span class="hotelPrice">$' + data[i].fields.price + '</span>';
                    }
                    else if (data[i].model == 'privateoffice.resort')
                    {
                        newdiv.setAttribute('onclick', 'showOther(this)')
                        newdiv.id = "resort_"+data[i].pk
                        resortResultList.insertBefore(newdiv, resortResultList.firstChild);
                        newdiv.innerHTML = data[i].fields.name;
                    }
                }
            }
        }
    )
}
function showOther(parent)
{
    var countryResultList = document.getElementById('searchCountry');
    var resortResultList = document.getElementById('searchResort');
    var hotelResultList = document.getElementById('searchHotel');
    if (currentResort != ''){
        currentResort.style.backgroundColor = '#fafafa';
    }
    currentResort = parent;
    parent.style.backgroundColor = selectedColor;
    parent_id = parent.id
    parent_pk = parent_id.substr(parent_id.indexOf('_') + 1)
    $.ajax
    (
        {
            url:        "/api/search/other/",
            type:       "POST",
            data:       parent_pk,
            success:    function(data)
            {
                //while(resortResultList.lastChild) {resortResultList.removeChild(resortResultList.lastChild);}
                while(hotelResultList.lastChild) {hotelResultList.removeChild(hotelResultList.lastChild);}
                for (var i=0; i<data.length; i++)
                {
                    newdiv = document.createElement('div');
                    newdiv.className = 'searchElement';
                    if (data[i].model == 'privateoffice.hotel')
                    {
                        newdiv.setAttribute('onclick', 'showParent(this)')
                        newdiv.id = "hotel_"+data[i].pk
                        hotelResultList.insertBefore(newdiv, hotelResultList.firstChild);
                        newdiv.innerHTML = data[i].fields.name + '<span class="hotelPrice">$' + data[i].fields.price + '</span>';
                    }
                    else if (data[i].model == 'privateoffice.country')
                    {
                        if (currentCountry == ''){
                            currentCountry = document.getElementById('country_'+data[i].pk)
                            currentCountry.style.backgroundColor=selectedColor;
                        }
                        else
                        {
                            currentCountry.style.backgroundColor="#fafafa"
                            currentCountry = document.getElementById('country_'+data[i].pk)
                            currentCountry.style.backgroundColor=selectedColor;
                        }
                    }
                }
            }
        }
    )
}
function showParent(child)
{
    var countryResultList = document.getElementById('searchCountry');
    var resortResultList = document.getElementById('searchResort');
    var hotelResultList = document.getElementById('searchHotel');
    if (currentHotel != ''){
        currentHotel.style.backgroundColor = '#fafafa';
    }
    currentHotel = child;
    child.style.backgroundColor = selectedColor;
    child_id = child.id;
    child_pk = child_id.substr(child_id.indexOf('_') + 1)
    selectedHitelPK = child_pk;
    $.ajax
    (
        {
            url:        "/api/search/parent/",
            type:       "POST",
            data:       child_pk,
            success:    function(data)
            {
                //while(resortResultList.lastChild) {resortResultList.removeChild(resortResultList.lastChild);}
                //while(hotelResultList.lastChild) {hotelResultList.removeChild(hotelResultList.lastChild);}
                for (var i=0; i<data.length; i++)
                {
                    //newdiv = document.createElement('div');
                    //newdiv.className = 'searchElement';
                    if (data[i].model == 'privateoffice.hotel')
                    {
                        selectedHotel = document.getElementById('selectedHotel');
                        selectedHotel.style.backgroundColor = '#3D9970';
                        selectedHotel.style.color = '#fff';
                        while(selectedHotel.lastChild) {selectedHotel.removeChild(selectedHotel.lastChild);}
                        newdiv = document.createElement('div');
                        newdiv.className = 'resultHotel';
                        newdiv.id = data[i].pk
                        selectedHotel.appendChild(newdiv, selectedHotel.firstChild);
                        //selectedHotel.insertAfter(newdiv, hotelResultList.firstChild);
                        //selectedHotel.innerHTML = newdiv
                        newdiv.innerHTML = 'Оформить заявку на ' + data[i].fields.name;
                    }
                    else if (data[i].model == 'privateoffice.country')
                    {
                        if (currentCountry == ''){
                            currentCountry = document.getElementById('country_'+data[i].pk)
                            currentCountry.style.backgroundColor=selectedColor;
                        }
                        else
                        {
                            currentCountry.style.backgroundColor="#fafafa";
                            currentCountry = document.getElementById('country_'+data[i].pk)
                            currentCountry.style.backgroundColor=selectedColor;
                        }
                    }
                }
            }
        }
    )
}
function addOrder()
{
    if (currentHotel != '')
    {
        currentHotel_pk =currentHotel.id
        currentHotel_pk = currentHotel_pk.substr(currentHotel_pk.indexOf('_') + 1)
        //alert(currentHotel_pk)
        $.ajax
        (
            {
                url:        "/api/addorder/",
                type:       "POST",
                data:       currentHotel_pk,
                success:    function(data)
                {
                    staff = document.getElementById('staffDiv');
                    //while(selectedHotel.lastChild) {selectedHotel.removeChild(selectedHotel.lastChild);}
                    //newdiv = document.createElement('div');
                    //newdiv.className = 'resultHotel';
                    //newdiv.id = data[i].pk
                    //selectedHotel.appendChild(newdiv, selectedHotel.firstChild);
                    //selectedHotel.insertAfter(newdiv, hotelResultList.firstChild);
                    //selectedHotel.innerHTML = newdiv
                    staff.innerHTML = data;
                }
            }
        )
    }
}
function confirmOrder()
{
    hotel = selectedHitelPK;
    firstname = document.getElementById('id_firstName').value;
    lastname = document.getElementById('id_lastName').value;
    email = document.getElementById('id_email').value;
    date_day = document.getElementById('id_date_day').value;
    date_mounth = document.getElementById('id_date_month').value;
    date_year = document.getElementById('id_date_year').value;
    nights = document.getElementById('id_nights').value;
    count = document.getElementById('id_count').value;
    //alert(date_year+'-'+date_mounth+'-'+date_day)
    query = {
        hotel:      hotel,
        firstname:  firstname,
        lastname:   lastname,
        email:      email,
        date:       date_year+'-'+date_mounth+'-'+date_day,
        nights:     nights,
        count:      count
    };
    $.ajax
    (
        {
            url:        "/api/order/confirm/",
            type:       "POST",
            data:       query,
            success:    function(data)
            {
                if (data == 'good') {
                    window.location.href = "/office/";
                } else {
                    alert(data);
                }
            }
        }
    )
}
function closeModalWindow()
{
    staff = document.getElementById('staffDiv');
    backWindow = document.getElementById('modalWindowBkg');
    objWindow = document.getElementById('modalWindowObj');
    staff.removeChild(backWindow);
    staff.removeChild(objWindow);
}

var selectedColor = '#7FDBFF'
var currentCountry = '';
var currentResort = '';
var currentHotel = '';
var selectedHitelPK = '';
