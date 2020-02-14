# accuracy
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_7m_sim01/ngc4303_7m_only_co21_na.accuracy.png /home/saito/Desktop/ssc_test/ngc4303_7m_sim01/ngc4303_7m_only_co21_na.accuracyb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_7m_sim02/ngc4303_7m_only_co21_na.accuracy.png /home/saito/Desktop/ssc_test/ngc4303_7m_sim02/ngc4303_7m_only_co21_na.accuracyb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_caf_sim01/ngc4303_7m+tp+caf_co21_na.accuracy.png /home/saito/Desktop/ssc_test/ngc4303_caf_sim01/ngc4303_7m+tp+caf_co21_na.accuracyb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_caf_sim02/ngc4303_7m+tp+caf_co21_na.accuracy.png /home/saito/Desktop/ssc_test/ngc4303_caf_sim02/ngc4303_7m+tp+caf_co21_na.accuracyb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cbf_sim01/ngc4303_7m+tp+cbf_co21_na.accuracy.png /home/saito/Desktop/ssc_test/ngc4303_cbf_sim01/ngc4303_7m+tp+cbf_co21_na.accuracyb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cbf_sim02/ngc4303_7m+tp+cbf_co21_na.accuracy.png /home/saito/Desktop/ssc_test/ngc4303_cbf_sim02/ngc4303_7m+tp+cbf_co21_na.accuracyb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.accuracy.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.accuracyb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.accuracy.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.accuracyb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.feather.accuracy.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.feather.accuracyb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.feather.accuracy.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.feather.accuracyb.png

#convert -crop 80x538+800+134 /home/saito/Desktop/ssc_test/ngc4303_7m_sim01/ngc4303_7m_only_co21_na.accuracy.png ./colorbar.png

convert +append -border 0x0 /home/saito/Desktop/ssc_test/ngc4303_7m_sim01/ngc4303_7m_only_co21_na.accuracyb.png /home/saito/Desktop/ssc_test/ngc4303_caf_sim01/ngc4303_7m+tp+caf_co21_na.accuracyb.png /home/saito/Desktop/ssc_test/ngc4303_cbf_sim01/ngc4303_7m+tp+cbf_co21_na.accuracyb.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.accuracyb.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.feather.accuracyb.png ./colorbar.png ./ngc4303_sim01_accuracy.png

convert +append -border 0x0 /home/saito/Desktop/ssc_test/ngc4303_7m_sim02/ngc4303_7m_only_co21_na.accuracyb.png /home/saito/Desktop/ssc_test/ngc4303_caf_sim02/ngc4303_7m+tp+caf_co21_na.accuracyb.png /home/saito/Desktop/ssc_test/ngc4303_cbf_sim02/ngc4303_7m+tp+cbf_co21_na.accuracyb.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.accuracyb.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.feather.accuracyb.png ./colorbar.png ./ngc4303_sim02_accuracy.png

rm -rf /home/saito/Desktop/ssc_test/ngc4303_*/*b.png ./colorbar.png

# image
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_7m_sim01/ngc4303_7m_only_co21_na.smooth.pbcor.png /home/saito/Desktop/ssc_test/ngc4303_7m_sim01/ngc4303_7m_only_co21_na.smooth.pbcorb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_7m_sim02/ngc4303_7m_only_co21_na.smooth.pbcor.png /home/saito/Desktop/ssc_test/ngc4303_7m_sim02/ngc4303_7m_only_co21_na.smooth.pbcorb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_caf_sim01/ngc4303_7m+tp+caf_co21_na.smooth.pbcor.png /home/saito/Desktop/ssc_test/ngc4303_caf_sim01/ngc4303_7m+tp+caf_co21_na.smooth.pbcorb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_caf_sim02/ngc4303_7m+tp+caf_co21_na.smooth.pbcor.png /home/saito/Desktop/ssc_test/ngc4303_caf_sim02/ngc4303_7m+tp+caf_co21_na.smooth.pbcorb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cbf_sim01/ngc4303_7m+tp+cbf_co21_na.smooth.pbcor.png /home/saito/Desktop/ssc_test/ngc4303_cbf_sim01/ngc4303_7m+tp+cbf_co21_na.smooth.pbcorb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cbf_sim02/ngc4303_7m+tp+cbf_co21_na.smooth.pbcor.png /home/saito/Desktop/ssc_test/ngc4303_cbf_sim02/ngc4303_7m+tp+cbf_co21_na.smooth.pbcorb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.smooth.pbcor.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.smooth.pbcorb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.smooth.pbcor.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.smooth.pbcorb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.feather.smooth.pbcor.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.feather.smooth.pbcorb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.feather.smooth.pbcor.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.feather.smooth.pbcorb.png

#convert -crop 80x538+800+134 /home/saito/Desktop/ssc_test/ngc4303_7m_sim01/ngc4303_7m_only_co21_na.smooth.pbcor.png ./colorbar.png

convert +append -border 0x0 /home/saito/Desktop/ssc_test/ngc4303_7m_sim01/ngc4303_7m_only_co21_na.smooth.pbcorb.png /home/saito/Desktop/ssc_test/ngc4303_caf_sim01/ngc4303_7m+tp+caf_co21_na.smooth.pbcorb.png /home/saito/Desktop/ssc_test/ngc4303_cbf_sim01/ngc4303_7m+tp+cbf_co21_na.smooth.pbcorb.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.smooth.pbcorb.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.feather.smooth.pbcorb.png ./colorbar.png ./ngc4303_sim01_image.png

convert +append -border 0x0 /home/saito/Desktop/ssc_test/ngc4303_7m_sim02/ngc4303_7m_only_co21_na.smooth.pbcorb.png /home/saito/Desktop/ssc_test/ngc4303_caf_sim02/ngc4303_7m+tp+caf_co21_na.smooth.pbcorb.png /home/saito/Desktop/ssc_test/ngc4303_cbf_sim02/ngc4303_7m+tp+cbf_co21_na.smooth.pbcorb.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.smooth.pbcorb.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.feather.smooth.pbcorb.png ./colorbar.png ./ngc4303_sim02_image.png

rm -rf /home/saito/Desktop/ssc_test/ngc4303_*/*b.png ./colorbar.png

# model
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_7m_sim01/ngc4303_7m_only_co21_na.model.png /home/saito/Desktop/ssc_test/ngc4303_7m_sim01/ngc4303_7m_only_co21_na.modelb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_7m_sim02/ngc4303_7m_only_co21_na.model.png /home/saito/Desktop/ssc_test/ngc4303_7m_sim02/ngc4303_7m_only_co21_na.modelb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_7m_sim01/ngc4303_7m_only_co21_na.model.png /home/saito/Desktop/ssc_test/ngc4303_caf_sim01/ngc4303_7m+tp+caf_co21_na.modelb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_7m_sim02/ngc4303_7m_only_co21_na.model.png /home/saito/Desktop/ssc_test/ngc4303_caf_sim02/ngc4303_7m+tp+caf_co21_na.modelb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cbf_sim01/ngc4303_7m+tp+cbf_co21_na.model.png /home/saito/Desktop/ssc_test/ngc4303_cbf_sim01/ngc4303_7m+tp+cbf_co21_na.modelb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cbf_sim02/ngc4303_7m+tp+cbf_co21_na.model.png /home/saito/Desktop/ssc_test/ngc4303_cbf_sim02/ngc4303_7m+tp+cbf_co21_na.modelb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.model.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.modelb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.model.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.modelb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.model.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.feather.modelb.png
convert -crop 629x629+228+51 /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.model.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.feather.modelb.png

#convert -crop 80x538+800+134 /home/saito/Desktop/ssc_test/ngc4303_7m_sim01/ngc4303_7m_only_co21_na.model.png ./colorbar.png

convert +append -border 0x0 /home/saito/Desktop/ssc_test/ngc4303_7m_sim01/ngc4303_7m_only_co21_na.modelb.png /home/saito/Desktop/ssc_test/ngc4303_caf_sim01/ngc4303_7m+tp+caf_co21_na.modelb.png /home/saito/Desktop/ssc_test/ngc4303_cbf_sim01/ngc4303_7m+tp+cbf_co21_na.modelb.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.modelb.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim01/ngc4303_7m+tp+cdf_co21_na.feather.modelb.png ./colorbar.png ./ngc4303_sim01_model.png

convert +append -border 0x0 /home/saito/Desktop/ssc_test/ngc4303_7m_sim02/ngc4303_7m_only_co21_na.modelb.png /home/saito/Desktop/ssc_test/ngc4303_caf_sim02/ngc4303_7m+tp+caf_co21_na.modelb.png /home/saito/Desktop/ssc_test/ngc4303_cbf_sim02/ngc4303_7m+tp+cbf_co21_na.modelb.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.modelb.png /home/saito/Desktop/ssc_test/ngc4303_cdf_sim02/ngc4303_7m+tp+cdf_co21_na.feather.modelb.png ./colorbar.png ./ngc4303_sim02_model.png

rm -rf /home/saito/Desktop/ssc_test/ngc4303_*/*b.png ./colorbar.png

# combine
convert -append -border 0x0 ./ngc4303_sim01_image.png ./ngc4303_sim01_model.png ./ngc4303_sim01_accuracy.png ./ngc4303_sim01.png
convert -append -border 0x0 ./ngc4303_sim02_image.png ./ngc4303_sim02_model.png ./ngc4303_sim02_accuracy.png ./ngc4303_sim02.png

