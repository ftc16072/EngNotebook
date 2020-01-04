<%def name="title()">Home Page - ftc16072</%def>
<%def name="head()"></%def>
<%inherit file = "base.mako"/>
% for dateItem in dateList:
<A HREF="\viewEntry?dateString=${dateItem}&destination=Print">${dateItem}</A>
% endfor
