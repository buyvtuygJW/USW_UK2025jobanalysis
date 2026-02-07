import streamlit as st# extra deps in research env for frontend
import pandas as pd

#fixed prepare.since v1 cache to 1 shot load dataset
Coltoanalyze="technical skill"#"extractedskills"/allskills=all,technical_skill=it skills&tools
@st.cache_data
def load_and_prepare_data(Coltoanalyze):
    df=pd.read_json("extractedandgrouped_jobsv3_oneshot.json")
    skills_df = df.explode("allskills")
    personalqualities={"activity","analytical","ambitious",'adaptable',"perceptive","detail-focused","detail orientated","detail-driven","curious","confident","commercial thinking","commercially minded","customer‑focused","creative","meticulous","communicate well","communication","collaborate","enjoys working with","forward-thinking","highly organized","great","dedicated","determined","diligent","embracing","enthusiastic","enjoys","forward thinking","punctual","problem solver","results-driven","team leadership","leader","strong","polite","upskilling","bright","cheerful",'self-motivated',"motivated","organised","passion","hard working","love","proactive","competent",'learner',"leadership","all-rounder","sociability","positive attitude","timely","insipiring colleagues","curious about wellbeing", "accuracy", "strategic", "highly organised", "scalable", "reliable", "collaborative", "customer-focused", "innovative", "compassionate", "committed", "fast-paced", "thrives", "passionate about", "quality", "care", "effective", "interpersonal", "clients", "wellbeing", "organisation", "others grow", "ability to",
                      "caring", "accurate records", "building relationships",
        "love creating great", "creative", "insightful", "problem-solver",
        "strong relationships", "resilient", "continuous improvement",
        "self-starter", "sharp eye for detail", "precision", "tech-savvy",
        "welsh", "adaptive", "teamwork", "empathy", "exceptional",
        "colleagues", "commercial", "work under pressure", "accountability","inspiring colleagues"
        "capable", "sharp", "understanding", "organized","commitment",
        "operational excellence", "focused", "highest standards",
        "energetic", "personable", "consistency", "building strong relationships",
        "fast-paced environment", "general", "confidentiality"}


    RESP_VERBS = {"support", "ensure","using", "assist", "manage","oversee", "perform", "handle","provide","develop","build","deliver","produce","lead","create","work","handling","building","customers","shaping", "driving", "maintain", "management", "agile", "hands-on", "compliance", "optimise", "team", "leading", "service", "decision-making", "leading a team", "driving performance", "process", "undertake", "define", "drive innovation", "lead the", "day-to-day", "liaise", "liaising", "prepare", "coordination", "admin", "facilitating", "operations", "delivery", "embedding", "planning", "organisational", "resolving", "adhering", "strategy", "performance",
                 "respond", "improving processes", "managing the processes",
        "communicating", "aligning", "mentor", "turn", "partnering",
        "actionable", "work collaboratively", "develop strong relationships",
        "carry", "responding", "improve", "prioritise", "updating",
        "compliance with", "provide support", "preparation", "influencing",
        "leading teams", "projects", "collection", "people", "identifying",
        "troubleshooting", "set", "team with", "promote", "improving",
        "accurate data", "workflows", "guiding", "making",
        "deliver a first class service", "testing", "building lasting client relationships",
        "assess", "elevate", "partner", "work flexibly", "adhere",
        "sourcing", "utilise", "co-ordinate", "work independently",
        "issues", "future", "advice", "input", "chain", "excellent communication",
        "engage", "overseeing", "lead & run projects", "strategic planning",
        "optimise data pipelines", "developing &", "embed", "clinicians",
        "travel", "managing"}

    skills_df["responsibility"] = skills_df["allskills"].where(skills_df["allskills"].isin(RESP_VERBS), None)
    skills_df["personal quality"] = skills_df["allskills"].where(skills_df["allskills"].isin(personalqualities))
    mask = (
        ~skills_df["allskills"].isin(personalqualities)
        & ~skills_df["allskills"].isin(RESP_VERBS)
    )
    skills_df["technical skill"] = skills_df["allskills"].where(mask, None)

    skill_counts = skills_df.groupby(["group","jobTitle",Coltoanalyze]).size().reset_index(name="count")
    return skills_df, skill_counts


skills_df, skill_counts = load_and_prepare_data(Coltoanalyze)
#streamlit
st.title("2025-2026 UK job analysis")

st.subheader("-Skill Lookup by Group (Micro Analysis)")

# Extract unique groups for ui
groups = sorted(skill_counts["group"].unique())
# Dropdown instead of number input
group_input = st.selectbox(
    "Choose a group",
    options=groups,
    index=groups.index(303) if 303 in groups else 0
)
# Filter
filtered = skills_df[skills_df["group"] == group_input][["jobTitle", "technical skill"]]

# Show results
st.subheader("Results")
st.dataframe(filtered)

#plot_data = skill_counts[skill_counts["group"]==group_input].set_index(Coltoanalyze)["count"]#way1
plot_data = ( skill_counts[skill_counts["group"] == group_input].groupby(Coltoanalyze)["count"].sum() )#should be faster way2

# Matplotlib figure
import matplotlib.pyplot as plt
#way1
#fig, ax = plt.subplots(figsize=(8, 5))#MUST use matplotlib API in streamlit to have the figure object
#plot_data.plot(kind="bar", ax=ax, title=f"Skills frequency for group {group_input}")#old way, but if has 200 skills all cramp in x limited size
#ax.set_ylabel("Count")

#way2 dynamic size, scrollable skillfreq
n = len(plot_data)
height=max(5, n * 0.3)# 0.3–0.4 per bar is a decent start height = 5.

fig, ax = plt.subplots(figsize=(8, height))#fixed since horizontal as number of count now
plot_data.plot(kind="barh", ax=ax, title=f"Skills frequency for group {group_input}")##Horizontal bars + scroll is often more readable.
ax.set_xlabel("Count")
from matplotlib.ticker import MaxNLocator
ax.xaxis.set_major_locator(MaxNLocator(integer=True))#forces the x-axis to use whole numbers only

# Display in Streamlit
st.pyplot(fig)#plt.show() just a api replace

# macro job analaysis 
st.subheader("-Macro job analysis-")

Coltomacroanalyze="technical skill"

toptittleforai="Artificial Intelligence"
ai_secondaryleveltittle1="Machine Learning (All)"

# AI subcategories (only for AI)
AICATEGORY_MAP = {
        "tensorflow": "Framework",
        "pytorch": "Framework",
        "scikit-learn": "Library",
        "keras": "Library",
    "pandas": "Library","numpy":"Library",
    
        "data": ai_secondaryleveltittle1,
    "data analysis": ai_secondaryleveltittle1,
    "data engineering": ai_secondaryleveltittle1,
    "data management": ai_secondaryleveltittle1,
        "nlp": ai_secondaryleveltittle1,
        "mlops": ai_secondaryleveltittle1,
    "deep learning": "Machine Learning",
    "rag":"Machine Learning",
    "llm":"deep learning",
    "generative ai": "deep learning",
    "machine learning": ai_secondaryleveltittle1,
    "ai": "Concept",
    "AI": "Concept",
    "artificial intelligence": ai_secondaryleveltittle1,
        #"ml": "Concept",
    "copilot": "3rd party AI",
    }

MISC_CATEGORY_MAP = {
    "excel": "Productivity",
    "power bi": "BI Tool",
    "tableau": "BI Tool",
    "airflow":"Data Integration",
        "azure data factory": "Data Integration",
    "databricks": "Data Platform",
    "snowflake":"Data Platform",
    "microsoft fabric": "Data Platform",
     "python":"Programming Languages",
        "java":"Programming Languages",
        "R":"Programming Languages",
    "c#":"Programming Languages",
    "typescript":"Programming Languages",
    "php":"Programming Languages",
    "kotlin":"Programming Languages",
    "html":"Web",
        "sql":"database",
        "aws":"Cloud",
        "azure":"Cloud",
        "gcp":"Cloud",
    "ms excel":"Office",#out of root
    "dynamic 365":"CRM &ERP",
    "salesforce":"CRM",
    "kubernetes":"DevOps,Container Orchestration",
    "docker":"DevOps,Container",
    "react":"Library",
    "vue":"Library",
}

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# treemap
@st.cache_data
def build_treemap(skills_df,Coltomacroanalyze, toptittleforai):
    skill_counts = skills_df[Coltomacroanalyze].value_counts().reset_index()#try without resetindex see if the result is stilla cc and speed gain.CANNOT emove reset index else throw>AttributeError: 'numpy.int64' object has no attribute 'str'  when>counts[Coltomacroanalyze].str.lower()#.str.strip()
    counts = skill_counts.copy(deep=True)#existing data,just to prevent edit.
    counts.columns = [Coltomacroanalyze, "count"]
    
    # normalize
    counts["skill_norm"] = str(counts[Coltomacroanalyze]).lower()#.str.strip()
    
    # top-level category
    counts["top_category"] = np.where(
        counts["skill_norm"].isin(AICATEGORY_MAP.keys()),
        toptittleforai,
        "Misc"
    )
    
    # subcategory logic
    def get_subcategory(skill):
        if skill in AICATEGORY_MAP:
            return AICATEGORY_MAP[skill]
        if skill in MISC_CATEGORY_MAP:
            return MISC_CATEGORY_MAP[skill]
        return "Other"
    
    counts["subcategory"] = counts["skill_norm"].apply(get_subcategory)
    
    # root node
    counts["root"] = "All Skills"
    fig = px.treemap(
        counts,
        path=["root", "top_category", "subcategory", Coltomacroanalyze],
        values="count",
        color="top_category",
        color_discrete_map={
            toptittleforai: "#4C72B0",
            "Misc": "#55A868",
        },
        title="High Demand Skill Hierarchy Treemap"
    )
    fig.update_layout(margin=dict(t=40, l=0, r=0, b=0))
    return fig

fig = build_treemap(skills_df,Coltomacroanalyze, toptittleforai)
# streamlit display
st.plotly_chart(fig, use_container_width=True)



