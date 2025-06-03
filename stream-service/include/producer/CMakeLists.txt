get_filename_component(module_name ${CMAKE_CURRENT_SOURCE_DIR} NAME)

file(GLOB SOURCE_FILES ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp)
add_library(${module_name} ${SOURCE_FILES} kafka_producer.h)

target_include_directories(${module_name} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})