for((i=1;i<=64;i++))
do
	echo "~/mysql -uroot video -e" '"'"select image_link_sign1,image_link_sign2,image_sign1,image_sign2 from page$i where from_type=5;"'"|'awk "'"'NR>1{print "update normal_url'$i' set image_sign1="$3",image_sign2="$4" where image_link_sign1="$1" and image_link_sign2="$2";"}'"'"
	echo "~/mysql -uroot video -e" '"'"select image_link_sign1,image_link_sign2,image_sign1,image_sign2 from page$i where from_type=3;"'"|'awk "'"'NR>1{print "update possible_url'$i' set image_sign1="$3",image_sign2="$4" where image_link_sign1="$1" and image_link_sign2="$2";"}'"'"
done
