xquery version "1.0-ml";

(: Done By Wisam Alhroub [171054] and Mohammed Samaheen [171004] :)

import module namespace search = 
  "http://marklogic.com/appservices/search"
  at "/MarkLogic/appservices/search/search.xqy";

for $uri in cts:uris((), ("eager"))
return xdmp:spawn-function(function() {
  for $author in fn:doc($uri)/PubmedArticle/MedlineCitation/Article/AuthorList/Author
  let $_ := xdmp:node-insert-child($author, <FullName>{$author/ForeName/text()}{" "}{$author/LastName/text()}</FullName>)
  return $author
});


(:for $uri in cts:uris((), ("eager"))
return xdmp:spawn-function(function() {
  for $date in fn:doc($uri)/PubmedArticle/MedlineCitation/DateCompleted
  let $_ := xdmp:node-insert-child($date, <FullDate>{$date/Year/text()}/{$date/Month/text()}/{$date/Day/text()}</FullDate>)
  return $date
});


declare variable $options :=
<options xmlns="http://marklogic.com/appservices/search">
  (: Facet config for Full Name :)
  <constraint name="FullName">
    <range type="xs:string" facet="true">
      <element name="FullName"/>
      <facet-option>limit=20</facet-option>
      <facet-option>frequency-order</facet-option>
      <facet-option>descending</facet-option>
    </range>
  </constraint>
  (: Facet config for Year :)
  <constraint name="Year" facet="true">
    <range type="xs:gYear">
      <path-index>/PubmedArticle/MedlineCitation/DateCompleted/Year</path-index>
      <facet-option>limit=20</facet-option>
      <facet-option>descending</facet-option>
    </range>
  </constraint>

  <extract-document-data selected="include">
    <extract-path>//Title</extract-path>
    <extract-path>//FullDate</extract-path>
  </extract-document-data>
  
  <searchable-expression>
     /PubmedArticle/(MedlineCitation | PubmedData/(History | PublicationStatus | ArticleIdList))
  </searchable-expression>

  <constraint name="ISSN">
    <value>
        <element name="ISSN"/>
    </value>
  </constraint>
  
  <constraint name="LN">
    <value>
        <element name="LastName"/>
    </value>
  </constraint>

  <constraint name="FN">
    <word>
      <element name="ForeName"/>
    </word>
  </constraint> 
  
 <search:operator name="sort">
   <search:state name="newest">
      <search:sort-order direction="descending" type="xs:date">
         <search:element name="FullDate"/>
      </search:sort-order>

   </search:state>
   
   <search:state name="oldest">
      <search:sort-order direction="ascending" type="xs:date">
         <search:element name="FullDate"/>
      </search:sort-order>
      <search:sort-order>
         <search:score/>
      </search:sort-order>
   </search:state>
   
   <search:state name="relevance">
      <search:sort-order>
         <search:score/>
      </search:sort-order>
   </search:state>
 </search:operator>
 
</options>;

search:search("the AND Year:2000", $options)

