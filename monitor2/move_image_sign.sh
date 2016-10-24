for((i=1;i<=64;i++))
do
	VM=given_page$i
	OU=page$i
	SQL="update ${VM},${OU} set ${VM}.image_sign1=${OU}.image_sign1,${VM}.image_sign2=${OU}.image_sign2 where"
	SQL="$SQL ${VM}.link_sign1=${OU}.link_sign1 and ${VM}.link_sign2=${OU}.link_sign2"
	SQL="$SQL and ${VM}.image_link_sign1=${OU}.image_link_sign1 and ${VM}.image_link_sign2=${OU}.image_link_sign2"
	SQL="$SQL and ${VM}.image_sign1=0 and ${VM}.image_sign2=0"
	SQL="$SQL and ${OU}.image_sign1!=0 and ${OU}.image_sign2!=0"
	SQL="$SQL and ${OU}.from_type=0"
	echo "$SQL ;"
done
