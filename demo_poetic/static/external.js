
(function(){
 /** @constructor */
function JqlObj()
{
    this.length = 0;
}

var rspaces = /\s+/;
var trimLeft = /^[\s\xA0]+/;
var trimRight = /[\s\xA0]+$/;
var rclass = /[\n\t]/g;

JqlObj.prototype = {
    hide: function()
    {
        for( var i = 0; i < this.length; i++ ) {
            this[i].style.display = 'none';
        }
        return this;
    },

    show: function()
    {
        for( var i = 0; i < this.length; i++ ) {
            this[i].style.display = 'block';
        }
        return this;
    },

    append: function( obj )
    {
        if ( this.length > 0 ) {
            for ( var i = 0; i < obj.length; i++ ) {
                this[0].appendChild( obj[i] );
            }
        }

        return this;
    },

    empty: function()
    {
        for ( var i = 0; i < this.length; i++ ) {
            while( this[i].firstChild !== null ) {
                this[i].removeChild( this[i].firstChild );
            }
        }

        return this;
    },

    text: function( str )
    {
        if ( this.length > 0 ) {
            while( this[0].firstChild !== null ) {
                this[0].removeChild( this[0].firstChild );
            }

            this[0].appendChild( document.createTextNode(str) );
        }

        return this;
    },

    html: function( str )
    {
        for( var i = 0; i < this.length; i++ ) {
            this[i].innerHTML = str;
        }
        return this;
    },

	addClass: function( value ) {
		if ( value && typeof value === "string" ) {
			var classNames = (value || "").split( rspaces );

			for ( var i = 0, l = this.length; i < l; i++ ) {
				var elem = this[i];

				if ( elem.nodeType === 1 ) {
					if ( !elem.className ) {
						elem.className = value;

					} else {
						var className = " " + elem.className + " ",
							setClass = elem.className;

						for ( var c = 0, cl = classNames.length; c < cl; c++ ) {
							if ( className.indexOf( " " + classNames[c] + " " ) < 0 ) {
								setClass += " " + classNames[c];
							}
						}
						elem.className = jQuery.trim( setClass );
					}
				}
			}
		}

		return this;
	},

	removeClass: function( value ) {
		if ( (value && typeof value === "string") || value === undefined ) {
			var classNames = (value || "").split( rspaces );

			for ( var i = 0, l = this.length; i < l; i++ ) {
				var elem = this[i];

				if ( elem.nodeType === 1 && elem.className ) {
					if ( value ) {
						var className = (" " + elem.className + " ").replace(rclass, " ");
						for ( var c = 0, cl = classNames.length; c < cl; c++ ) {
							className = className.replace(" " + classNames[c] + " ", " ");
						}
						elem.className = jQuery.trim( className );

					} else {
						elem.className = "";
					}
				}
			}
		}

		return this;
	},

    each: function( fn )
    {
        for( var i = 0; i < this.length; i++ ) {
            fn(this[i]);
        }
    },

    focus: function()
    {
        if ( this.length > 0 ) {
            this[0].focus();
        }
        return this;
    },
    
    css: function(name, value) {
        // todo: handle '-'
        for( var i = 0; i < this.length; i++ ) {
            this[i].style[name] = "" + value;
        }
    }
};

//Returns true if it is a DOM element    
function isElement(o){
      return (
        typeof HTMLElement === "object" ? o instanceof HTMLElement : //DOM2
        typeof o === "object" && 
            (o.nodeType === 1 && typeof o.nodeName==="string") ||
            o.nodeType === 3
    );
}

function jqlCreate( obj, type )
{
    obj[0] = document.createElement(type);
    obj.length = 1;
}

function jqlSelectId( obj, id )
{
    var element = document.getElementById( id );
    if ( element !== null ) {
        obj[0] = element;
        obj.length = 1;
    }
}

function parse(selector)
{
    var re_id = /#(.*)$/;
    var elem_id = /^<\s*([a-zA-Z0-9]+).*>$/;

    var obj = new JqlObj();
    var mymatch;

    if ( isElement( selector ) ) {
        obj[0] = selector;
        obj.length = 1;

    // if it's an id,
    } else if( ( mymatch = re_id.exec( selector ) ) !== null ) {
        jqlSelectId( obj, mymatch[1] );

    // if it's a new element,
    } else if ( ( mymatch = elem_id.exec( selector ) ) !== null ) {
        jqlCreate( obj, mymatch[1] );

    } else {
        alert("Error: can't parse selector: " + selector + " (" +
                selector.nodeType );
    }

    return obj;
}

function jQuery(selector)
{
    var obj = parse( selector );

    return obj;
    
}

jQuery.trim = function( text ) {
        return text === null ?
            "" :
            text.toString().replace( trimLeft, "" ).replace( trimRight, "" );
};

$ = jQuery;

var scripts = document.getElementsByTagName('script'),
    script = scripts[scripts.length - 1];
var resultDiv = document.createElement("div");
script.parentNode.insertBefore( resultDiv, script );
var clearDiv = document.createElement("div");
clearDiv.style.clear = "both";
script.parentNode.insertBefore( clearDiv, resultDiv.nextSibling );

var MaxResults = 50;
var AjaxLoader = "https://rhymebrain.com/ajax-loader.gif";
var TextColour = null;

if ( "RhymeBrainMaxResults" in window ) {
    MaxResults = window["RhymeBrainMaxResults"];
}
if ( "RhymeBrainLoadingImage" in window ) {
    AjaxLoader = window["RhymeBrainLoadingImage"];
}
if ( "RhymeBrainTextColour" in window ) {
    TextColour = window["RhymeBrainTextColour"];
}
var img = document.createElement("img");
img.src = AjaxLoader;

function setStyle(div)
{
    $(div).addClass("RhymeBrainResult");
    div.style.margin = "0px";
    div.style.cssFloat = "left";
    div.style.padding = "0.5em 0.5em 0.5em 0em";
    div.style.width = "10em";

    if ( TextColour !== null ) {
        div.style.color = TextColour;
    }
}

function setH4Style(h4)
{
    $(h4).addClass("RhymeBrainHeader");
    h4.style.clear = "both";
    h4.style.paddingTop = "1em";
    h4.style.marginBottom = "0";

    if ( TextColour !== null ) {
        h4.style.color = TextColour;
    }
}

function display(words, div)
{
    var resultDiv = $(div);
    resultDiv.empty();

    var i;

    if ( words.length === 0 ) {
        resultDiv.text("No rhymes were found.");
    }

    var highest;
    var wordclass = "wordpanel";
    var firstSeparator = false;

    for( i = 0; i < words.length; i++ ) {

        if ( highest === undefined ) {
            highest = words[i]["score"];
        }

        div = $("<div>").text(words[i]["word"]);
        setStyle(div[0]);
        if ( words[i]["score"] !== highest ) {
            // var h1 = $("<h4>").text("");
            if ( firstSeparator ) {
                firstSeparator = false;
            }
            // setH4Style(h1[0]);
            
            // resultDiv.append( h1 );
            highest = words[i]["score"];

        }
        div[0].t = words[i]["word"];

        resultDiv.append(div);
    }

}

function RhymeBrainSubmit()
{
    var input = document.getElementById("RhymeBrainInput");
    var word = input.value;

    $(resultDiv).empty();
    resultDiv.appendChild( img );

    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src = "https://rhymebrain.com/talk?function=getRhymes" +
        "&word=" + encodeURIComponent(word) +
        "&maxResults=" + MaxResults + 
        "&jsonp=RhymeBrainResponse";

    document.body.appendChild(script);
}


function RhymeBrainResponse(data)
{
    display(data, resultDiv );
}


window.RhymeBrainResponse = RhymeBrainResponse;
window.RhymeBrainSubmit = RhymeBrainSubmit;


}());
