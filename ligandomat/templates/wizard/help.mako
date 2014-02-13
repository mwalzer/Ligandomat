<%inherit file='ligandomat:templates/layout_wizard.mako'/>

<table>
	<tr>
		<td >
		</td>
		<td>
		This wizard collects meta data abourt your mass spectrometry run. A huge amount of peptides have been collected yet. For digital documentation and access of this data we implemented the Ligandomat.
		</td>
	</tr>
	<tr>
		<td class='helpheader'> Source
		</td>
		<td class='helpheader'> * * * 
		</td>
		<td class='helpheader'> * * * 
		</td>
	</tr>
	<tr>
		<td> name
		</td>
		<td> The name of a specific source should allow to directly see wheather it comes from benign or tumor tissue. Therefore, please continue the nomenclature of specificname_benign or specificname_tumor. 
		</td>
		<td> ex. HCC16_benign, RCC001_tumor
		</td>
	</tr>
	<tr>
		<td> Typings
		</td>
		<td> You can add up to 6 Typings for MHC-I molekules. For each time you need to select the allele form a given drop down box (not every number occurs, for example B*23). You can refine the typing with the text box right next to the drop down menu. There are only certain inputs valid: [number], [:number], [:III:II:IIL] where I stands for a digit and L for a letter.
		</td>
		<td> ex. [5], [05], [005], [:05], [:005:44:12B]
		</td>
	</tr>
	<tr>
		<td> organ
		</td>
		<td> Choose the used organ by the drop down menu. If the organ happens to not appear in the list, please see one of the administrators.
		</td>
		<td> Possibilities : Liver / !!!
		</td>
	</tr>
	<tr>
		<td> organism
		</td>
		<td> Choose the organism of the source by the drop down menu. If it happens to not appear in the list, please see one of the administrators.
		</td>
		<td> Possibilities : Human / !!!
		</td>
	</tr>
	<tr>
		<td> tissue
		</td>
		<td> Here you should specify the tissue.
		</td>
		<td> Possibilities : Adjacent benign / !!!
		</td>
	</tr>
	<tr>
		<td> dignity
		</td>
		<td> Here you should specify the dignity.
		</td>
		<td> Possibilities :  / !!!
		</td>
	</tr>
	<tr>
		<td> celltype
		</td>
		<td> This field is a Textbox. You can describe some specialities about the celltype
		</td>
		<td> !!!
		</td>
	</tr>
	<tr>
		<td> comment
		</td>
		<td> If you want to add anything else, this is the correct field
		</td>
		<td> ex. Patients medical records
		</td>
	</tr>
	
	
	
	
	<tr>
		<td class='helpheader'> Preparation
		</td>
		<td class='helpheader'> * * * 
		</td>
		<td class='helpheader'> * * * 
		</td>
	</tr>
	<tr>
		<td class='helpheader'> Mass spectrometry
		</td>
		<td class='helpheader'> * * * 
		</td>
		<td class='helpheader'> * * * 
		</td>
	</tr>
	<tr>
		<td> 
		</td>
	</tr>
<table>

<style type="text/css">

table {
	width:800px;
}

td {
}

.helpheader{
	font-size:20px;
	height: 50px;
	background-color:#E8E8E8;
	text-align:center;

}

</style>



