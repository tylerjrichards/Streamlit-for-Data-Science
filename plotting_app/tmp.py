import numpy as np
import pandas as pd
import streamlit as st

st.title("MEGA APP")
st.write("This app exists to test out all the st commands we possibly can in one go")

st.balloons()
st.snow()

st.write("# input tests")
st.text_input("textbox")
st.number_input("number")
st.slider("slider")
st.button("button")
st.checkbox("checkbox")
st.radio("radio", ["cat", "dog"])
st.selectbox("selectbox", ["cat", "dog"])
st.multiselect("multiselect", ["cat", "dog"])
st.select_slider("select slider", ["cat", "dog"])
st.text_area("text area")
st.date_input("date input")
st.time_input("time input")
st.file_uploader("file input")
st.write("file uploader fails with 404 code")
st.color_picker("color picker")
text_contents = """This is some text"""
st.download_button("Download some text", text_contents)
st.camera_input("cam input")

st.write("# text elements")
st.write("st write")
st.markdown("hello markdown")
st.header("hello header")
st.subheader("hello subheader")
st.caption("hello caption")
st.code("a = 1234")
st.text("hello text")
st.latex("\int a x^2 \,dx")
"""
hello magic
"""

st.write("# data display elements")
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.dataframe(chart_data)
st.table(chart_data)
st.metric("Metric", 42, 2)
st.write("st json")
st.json(chart_data.head().to_dict())


st.write("# chart elements")
st.line_chart(chart_data)
st.area_chart(chart_data)
st.bar_chart(chart_data)

map_df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=["lat", "lon"]
)


"""
st.map does not work currently
"""

"""
matplotlib, plotly, bokeh, pydeck, graphviz, and vegalite will be available when we turn on the anaconda packages in q4
"""

st.write("# Media elements")
image_nums = np.random.randint(255, size=(144, 144), dtype=np.uint8)

st.write("st image does not work currently")
st.image(image_nums)

fs = 44100
data = np.random.uniform(-1, 1, fs)
st.audio(data)

st.video(data)
st.image(image_nums)

st.write("# layouts and containers")

st.sidebar.write("sidebar test")

a, b = st.columns(2)
with b:
    st.write("col check, should be second column")

with a:
    st.write("col check, should be first column")

taba, tabb = st.tabs(["tab a", "tab b"])
tabb.write("tab b test")

with st.expander("open to see expander"):
    st.write("works!")

c = st.container()

c.write("should write in the container")

a = st.empty()

a.write("should write in the empty block")


st.write("# display progress and status")

st.write("progress bar test")
my_bar = st.progress(0)
for percent_complete in range(100):
    my_bar.progress(percent_complete + 1)


with st.spinner("Wait!"):
    st.write("hey")

st.error("st error")
st.warning("st warning")
st.info("st info")
st.success("st success")
e = RuntimeError("example of error")
st.exception(e)
